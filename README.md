# Information Security Project: Encryption, Decryption, and Password Strength Analyzer

This project focuses on implementing encryption and decryption algorithms, along with a comprehensive password strength analyzer. The encryption/decryption system supports images, text, and text files, while the password analyzer assesses password strength and checks for breaches.

## Table of Contents
1. [Encryption & Decryption Algorithms](#encryption--decryption-algorithms)
2. [Password Strength Analyzer](#password-strength-analyzer)
3. [Technologies Used](#technologies-used)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [Group Members](#group-members)

## Encryption & Decryption Algorithms

This project supports multiple encryption algorithms for both text and image encryption/decryption.

### Image Encryption/Decryption
- **AES**
- **Fernet**
- **ChaCha20**

### Text Encryption/Decryption
- **AES**
- **Fernet**
- **Caesar Cipher**

### Text File Encryption/Decryption
- **RSA**

## Password Strength Analyzer

The Password Analyzer analyzes the strength of a given password using the `zxcvbn` library and provides feedback on the password's strength, time to crack, and patterns detected. It also checks if the password is among the most common passwords and whether it has been compromised in any data breaches.

### Key Features:
- **Strength Evaluation**: Ranges from "Very Weak" to "Very Strong."
- **Password Entropy**: Provides an estimate of the password's entropy using `zxcvbn`.
- **Crack Time Estimation**: Estimates the time it would take to crack the password using various attack scenarios.
- **Pattern Detection**: Identifies common patterns such as repetitive characters and sequential numbers.
- **Common Password Check**: Compares the password against a list of commonly used passwords.
- **Breach Check**: Uses the "Have I Been Pwned" API to check if the password has appeared in any known data breaches.

## Technologies Used
- **AES** for symmetric encryption/decryption.
- **Fernet** for authenticated encryption/decryption.
- **ChaCha20** for symmetric encryption.
- **RSA** for asymmetric encryption.
- **Caesar Cipher** for simple text encryption.
- **zxcvbn** for password strength estimation.
- **requests** for checking passwords in the "Have I Been Pwned" database.
- **PyQt5** for the user interface (UI).

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ufaq222/IS_Project.git
cd IS_Project
```

### 2. Install the Required Dependencies
```bash
pip install -r requirements.txt
```

The following libraries are used in the project:
- `base64`
- `cryptography`
- `re`
- `math`
- `random`
- `string`
- `datetime`
- `hashlib`
- `json`
- `requests`
- `time`
- `zxcvbn`
- `logging`
- `PyQt5`

### 3. Run the UI
To run the application with the user interface, execute the following command:
```bash
python ui.py
```

**Note:** Ensure you have the necessary files for common password lists and encryption key generation.

## Usage

### Encrypt and Decrypt Images
- Use AES, Fernet, or ChaCha20 algorithms by calling appropriate functions to encrypt or decrypt image files.

### Encrypt and Decrypt Text
- Use AES, Fernet, or Caesar Cipher to encrypt and decrypt text.

### Encrypt and Decrypt Text Files
- Use RSA encryption/decryption methods for text file-based operations.

## Group Members
- **[Khadija Saeed]** 
- **[Hira Sohail]** 
- **[Ufaq Hafeez]** 
