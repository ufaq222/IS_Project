import re
import math
import random
import string
from datetime import datetime
import hashlib
import json
import requests
import time
from zxcvbn import zxcvbn
import logging

# Configure logging for production use
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PasswordAnalyzer:
    def __init__(self, common_passwords_file='common_passwords.txt', hibp_rate_limit=1.5):
        self.common_passwords = self.load_common_passwords(common_passwords_file)
        self.hibp_rate_limit = hibp_rate_limit  # Seconds between HIBP requests
        self.last_hibp_request = 0
        self.special_chars = string.punctuation  # Customizable special character pool

    def load_common_passwords(self, filename):
        """Load common passwords from a file or use a fallback set."""
        try:
            with open(filename, 'r') as f:
                passwords = {line.strip().lower() for line in f if line.strip()}
                logger.info(f"Loaded {len(passwords)} common passwords from {filename}")
                return passwords
        except FileNotFoundError:
            logger.warning(f"Common passwords file {filename} not found. Using fallback list.")
            return {
                'password', '123456', '123456789', 'qwerty', 'abc123',
                'password1', 'admin', 'welcome', 'monkey', 'sunshine',
                'letmein', 'football', 'iloveyou', '123abc', 'admin123'
            }

    def analyze_password(self, password):
        """Analyze a password and return a detailed report."""
        if not password:
            return {
                'strength': 'None',
                'time_to_crack': 'Instantly',
                'character_counts': {},
                'total_characters': 0,
                'requirements': {},
                'is_common': False,
                'entropy': 0,
                'zxcvbn_score': 0,
                'patterns_detected': [],
                'review': 'No password provided',
                'pwned': False,
                'pwned_message': 'No password provided to check breaches'
            }

        # Core analysis
        zxcvbn_result = self.calculate_zxcvbn(password)
        strength = self.map_zxcvbn_score(zxcvbn_result['score'])
        entropy = zxcvbn_result['guesses_log2']  # zxcvbn's entropy estimate
        patterns = self.detect_patterns(password)
        time_to_crack = self.estimate_crack_time(zxcvbn_result['guesses'], password, patterns)
        char_counts = self.count_character_types(password)
        total_chars = len(password)
        requirements = self.check_requirements(password)
        is_common = password.lower() in self.common_passwords
        review = self.get_password_review(strength, is_common, patterns)
        pwned, pwned_message = self.is_password_pwned(password)

        return {
            'strength': strength,
            'time_to_crack': time_to_crack,
            'character_counts': char_counts,
            'total_characters': total_chars,
            'requirements': requirements,
            'is_common': is_common,
            'entropy': entropy,
            'zxcvbn_score': zxcvbn_result['score'],
            'patterns_detected': patterns,
            'review': review,
            'pwned': pwned,
            'pwned_message': pwned_message
        }

    def get_password_review(self, strength, is_common, patterns):
        """Generate feedback based on password analysis."""
        if is_common:
            return "This password is too common and easily guessable. Choose a unique, random password."
        if patterns:
            return f"Weak password: detected patterns ({', '.join(patterns)}). Use a more random combination."
        
        reviews = {
            "Very Weak": "Very poor security. Use a longer password with mixed characters.",
            "Weak": "Weak password. Add symbols, numbers, and mixed case for better security.",
            "Moderate": "Moderate strength. Increase length or complexity for better protection.",
            "Strong": "Strong password. Consider adding a few more characters.",
            "Very Strong": "Excellent password! Ensure you store it securely."
        }
        return reviews.get(strength, "Enter a valid password to get feedback.")

    def calculate_zxcvbn(self, password):
        """Use zxcvbn to analyze password strength."""
        try:
            result = zxcvbn(password)
            return {
                'score': result['score'],  # 0 (weak) to 4 (strong)
                'guesses': result['guesses'],  # Estimated guesses needed
                'guesses_log2': math.log2(max(result['guesses'], 1))  # Entropy estimate
            }
        except Exception as e:
            logger.error(f"zxcvbn analysis failed: {str(e)}")
            return {'score': 0, 'guesses': 1, 'guesses_log2': 0}

    def map_zxcvbn_score(self, score):
        """Map zxcvbn score (0-4) to strength categories."""
        mapping = {
            0: "Very Weak",
            1: "Weak",
            2: "Moderate",
            3: "Strong",
            4: "Very Strong"
        }
        return mapping.get(score, "Very Weak")

    def count_character_types(self, password):
        """Count the number of each character type."""
        return {
            'lower': sum(1 for c in password if c.islower()),
            'upper': sum(1 for c in password if c.isupper()),
            'digits': sum(1 for c in password if c.isdigit()),
            'special': len([c for c in password if not c.isalnum()])
        }

    def check_requirements(self, password):
        """Check if password meets common requirements."""
        length = len(password)
        return {
            'length': length >= 8,
            'min_12_chars': length >= 12,
            'upper': any(c.isupper() for c in password),
            'lower': any(c.islower() for c in password),
            'digit': any(c.isdigit() for c in password),
            'special': bool(re.search(r'[^a-zA-Z0-9]', password))
        }

    def detect_patterns(self, password):
        """Detect repetitive or sequential patterns."""
        patterns = []
        # Check for repetitive characters (e.g., "aaa")
        if re.search(r'(.)\1{2,}', password):
            patterns.append("repetitive characters")
        # Check for sequential numbers (e.g., "123")
        if re.search(r'(?:012|123|234|345|456|567|678|789|987|876|765|654|543|432|321|210)', password):
            patterns.append("sequential numbers")
        # Check for sequential letters (e.g., "abc")
        if re.search(r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password, re.IGNORECASE):
            patterns.append("sequential letters")
        return patterns

    def estimate_crack_time(self, guesses, password, patterns):
        """Estimate time to crack, using online scenario by default and offline_hybrid for repetitive patterns."""
        if guesses <= 1:
            logger.info("Crack time: Instantly for all scenarios (guesses <= 1)")
            return "Instantly"

        # Convert Decimal to float
        guesses = float(guesses)

        # Attack scenario parameters (based on 2025 hardware and tools)
        attack_speeds = {
            'offline_bruteforce': 1e11,  # 100 billion guesses/sec (e.g., hashcat, MD5, 8x RTX 4090)
            'offline_hybrid': 1e7,       # 10 million guesses/sec (dictionary + mangling rules)
            'online': 10                 # 10 guesses/sec (throttled online login)
        }

        # Calculate brute-force guesses separately (for comparison)
        pool_size = 0
        if any(c.islower() for c in password): pool_size += 26
        if any(c.isupper() for c in password): pool_size += 26
        if any(c.isdigit() for c in password): pool_size += 10
        if re.search(r'[^a-zA-Z0-9]', password): pool_size += 32
        bruteforce_guesses = pool_size ** len(password) if pool_size > 0 else 1

        # Use zxcvbn guesses for hybrid and online (accounts for patterns/dictionary)
        # Use min of zxcvbn and bruteforce guesses for offline_bruteforce
        effective_guesses = {
            'offline_bruteforce': min(guesses, bruteforce_guesses),
            'offline_hybrid': guesses,
            'online': guesses
        }

        # Calculate crack times for all scenarios (for logging)
        crack_times = {}
        for scenario, speed in attack_speeds.items():
            seconds = effective_guesses[scenario] / speed
            if seconds < 1:
                crack_times[scenario] = 'Instantly'
            elif seconds < 60:
                crack_times[scenario] = f"{seconds:.2f} seconds"
            elif seconds < 3600:
                crack_times[scenario] = f"{seconds/60:.2f} minutes"
            elif seconds < 86400:
                crack_times[scenario] = f"{seconds/3600:.2f} hours"
            elif seconds < 31536000:
                crack_times[scenario] = f"{seconds/86400:.2f} days"
            else:
                crack_times[scenario] = f"{seconds/31536000:.2f} years"

        # Log all scenario results for debugging
        logger.info(f"Crack times for '{password}': {json.dumps(crack_times)}")

        # Return offline_hybrid for repetitive patterns, otherwise online
        if "repetitive characters" in patterns:
            logger.info(f"Using offline_hybrid crack time for '{password}' due to repetitive patterns")
            return crack_times['offline_hybrid']
        return crack_times['online']

    def generate_password(self, length=12, include_special=True, special_chars=None):
        """Generate a random password."""
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        special = special_chars or self.special_chars

        # Ensure at least one of each type
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
        ]
        if include_special:
            password.append(random.choice(special))

        # Fill remaining
        all_chars = lower + upper + digits
        if include_special:
            all_chars += special

        password.extend(random.choice(all_chars) for _ in range(length - len(password)))
        random.shuffle(password)
        return ''.join(password)

    def is_password_pwned(self, password):
        """Check if password appears in HIBP database with rate limiting."""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."

        # Enforce rate limiting
        elapsed = time.time() - self.last_hibp_request
        if elapsed < self.hibp_rate_limit:
            time.sleep(self.hibp_rate_limit - elapsed)

        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]

        try:
            response = requests.get(
                f'https://api.pwnedpasswords.com/range/{prefix}',
                headers={'User-Agent': 'PasswordAnalyzer'},
                timeout=5
            )
            self.last_hibp_request = time.time()
            if response.status_code != 200:
                logger.error(f"HIBP API returned status {response.status_code}")
                return False, "Error checking pwned passwords."

            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    return True, f"This password has appeared in {count} known data breaches!"
            return False, "This password has not been found in known breaches."
        except Exception as e:
            logger.error(f"Failed to check HIBP: {str(e)}")
            return False, f"Failed to check pwned status: {str(e)}"

    def set_special_chars(self, special_chars):
        """Set custom special character pool for password generation."""
        if not all(c in string.punctuation for c in special_chars):
            raise ValueError("Special characters must be punctuation.")
        self.special_chars = special_chars
        logger.info(f"Set special character pool to: {special_chars}")