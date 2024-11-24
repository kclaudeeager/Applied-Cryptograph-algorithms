# Myaesprog

Myaesprog is a Python script that performs AES encryption and decryption on files using a specified key. The script supports both encryption and decryption modes and uses a custom header format to store metadata about the encrypted files.

## Features

- AES encryption and decryption using a 32-byte key.
- Custom 80-byte header format for storing metadata.
- Supports encryption of files with filenames up to 59 characters.
- Automatically handles padding to ensure the payload is a multiple of 16 bytes.
- Basic error checking for key file size and filename length.
- Prevents overwriting existing files during decryption by prefixing "x_" to the output filename if it already exists.

## Requirements

- Python 3.x
- numpy
- cryptography

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required Python packages using pip:

```sh
pip install numpy cryptography
```
Or 

```sh
pip install -r requirements.txt
```

## Usage

### Encryption

To encrypt a file, use the following command:

```sh
python myaesprog.py <input_file> <output_file> <key_file>
```

- `<input_file>`: The file to be encrypted.
- `<output_file>`: The name of the output file to store the encrypted data.
- `<key_file>`: A file containing the 32-byte base64 encoded encryption key.

Example:

```sh
python myaesprog.py soccer.jpg soccer.aes mykey.txt
```

### Decryption

To decrypt a file, use the following command:

```sh
python myaesprog.py <input_file> <key_file>
```

- `<input_file>`: The encrypted file to be decrypted (must end with `.aes`).
- `<key_file>`: A file containing the 32-byte base64 encoded decryption key.

Example:

```sh
python myaesprog.py soccer.aes mykey.txt
```

### Notes

- The script determines whether to encrypt or decrypt based on the number of command-line arguments.
- The input filename for encryption must be 59 characters or less.
- The key file must contain exactly 32 bytes when decoded from base64.
- During decryption, if the output filename already exists, the script will prefix "x_" to the filename to prevent overwriting.

## Example

1. Create a key file with a 32-byte base64 encoded key:

```sh
python aes_demo.py
```

2. Encrypt a file:

```sh
python myaesprog.py soccer.jpg soccer.aes mykey.txt
```

3. Decrypt the file:

```sh
python myaesprog.py soccer.aes mykey.txt
```
## Author

Claude Kwizera

---