#!/usr/bin/env python3
import numpy as np
import sys
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import struct

class Myaesprog:
    """
    A class to perform AES encryption and decryption using a specified key.
    Attributes:
    key (bytes): The encryption key.
    __cipher (Cipher): The AES cipher object.
    __encryptor (CipherContext): The AES encryption context.
    __decryptor (CipherContext): The AES decryption context.
    Methods:
    __init__(key):
        Initializes the Myaesprog object with the given key.
    encrypt_blk(data_block):
        Encrypts a single block of data.
    decrypt_blk(data_block):
        Decrypts a single block of data.
    encrypt(plaintext, original_filename):
        Encrypts the given plaintext and returns the ciphertext.
    decrypt(ciphertext):
        Decrypts the given ciphertext and returns the original filename and plaintext.
    finalize():
        Finalizes the encryption and decryption contexts.
    read_key_file(filename):
        Reads the key from the specified file and returns it as a numpy array.
    encrypt_file(input_file, output_file, key_file):
        Encrypts the contents of the input file and writes the ciphertext to the output file.
    decrypt_file(input_file, key_file):
        Decrypts the contents of the input file and writes the plaintext to the output file.
    run_main():
        Main method to handle command-line arguments for encryption and decryption.
    """
    def __init__(self, key):
        self.key = key
        self.__cipher = Cipher(algorithms.AES(self.key), modes.ECB())
        self.__encryptor = self.__cipher.encryptor()
        self.__decryptor = self.__cipher.decryptor()
    
    def encrypt_blk(self, data_block):
        return np.frombuffer(self.__encryptor.update(data_block), np.uint8, -1)
    
    def decrypt_blk(self, data_block):
        return np.frombuffer(self.__decryptor.update(data_block), np.uint8, -1)

    def encrypt(self, plaintext, original_filename):
        # Create 80-byte header
        nonce = os.urandom(16)
        filename_b = original_filename.encode('utf-8')
        filename_len = len(filename_b)
        
        if filename_len > 59:
            raise ValueError("Filename must be 59 characters or less")
        
        # Create unencrypted header
        header = bytearray(80)
        header[0:16] = nonce
        header[16] = filename_len
        header[17:17+filename_len] = filename_b
        payload_len = len(plaintext)
        header[76:80] = struct.pack('>I', payload_len)  # Encode payload length as big-endian
        
        # Encrypt the header using CBC mode
        encrypted_header = bytearray()
        prev_block = nonce
        for i in range(0, 80, 16):
            block = header[i:i+16]
            xored_block = bytes(a ^ b for a, b in zip(block, prev_block))
            encrypted_block = self.encrypt_blk(xored_block)
            encrypted_header.extend(encrypted_block)
            prev_block = encrypted_block
        
        # Pad plaintext to be multiple of 16 bytes
        padding_len = 16 - (payload_len % 16)
        padded_plaintext = plaintext + bytes([padding_len]) * padding_len
        
        # Encrypt payload using CBC mode
        encrypted_payload = bytearray()
        prev_block = encrypted_header[-16:]  # Use last block of encrypted header as Initialization Vector (IV)
        for i in range(0, len(padded_plaintext), 16):
            block = padded_plaintext[i:i+16]
            xored_block = bytes(a ^ b for a, b in zip(block, prev_block))
            encrypted_block = self.encrypt_blk(xored_block)
            encrypted_payload.extend(encrypted_block)
            prev_block = encrypted_block
        
        # Combine encrypted header and encrypted payload
        ciphertext = encrypted_header + encrypted_payload
        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) < 80:
            raise ValueError("Ciphertext is too short to contain header")

        # Decrypt the header
        encrypted_header = ciphertext[:80]
        decrypted_header = bytearray()
        prev_block = b'\0' * 16  # IV for the first block
        for i in range(0, 80, 16):
            encrypted_block = encrypted_header[i:i+16]
            decrypted_block = self.decrypt_blk(encrypted_block)
            decrypted_header.extend(bytes(a ^ b for a, b in zip(decrypted_block, prev_block)))
            prev_block = encrypted_block

        # Extract header information
        nonce = decrypted_header[:16]
        print("Nonce: ", nonce)
        filename_len = decrypted_header[16]
        print("Filename length: ", filename_len)
        if filename_len > 59:
            raise ValueError("Filename length in header is invalid")

        original_filename = decrypted_header[17:17+filename_len].decode('utf-8', errors='replace')
        payload_len = struct.unpack('>I', decrypted_header[76:80])[0]

        # Decrypt payload
        plaintext = bytearray()
        prev_block = encrypted_header[-16:]  # Last block of encrypted header
        for i in range(80, len(ciphertext), 16):
            encrypted_block = ciphertext[i:i+16]
            decrypted_block = self.decrypt_blk(encrypted_block)
            plaintext.extend(bytes(a ^ b for a, b in zip(decrypted_block, prev_block)))
            prev_block = encrypted_block

        # Remove padding
        plaintext = plaintext[:payload_len]

        return original_filename, bytes(plaintext)

    def finalize(self):
        self.__decryptor.finalize()
        self.__encryptor.finalize()
    
    @staticmethod
    def read_key_file(filename):
        with open(filename, 'rb') as fd:
            key_b = base64.b64decode(fd.read().strip())
        if len(key_b) != 32:
            raise ValueError("Key file must contain exactly 32 bytes")
        return np.frombuffer(key_b, np.uint8, -1)

    def validate_key_file(self, key_file):
        with open(key_file, 'rb') as f:
            key = base64.b64decode(f.read().strip())
        if len(key) != 32:
            raise ValueError("Key file must contain exactly 32 bytes when decoded")
    
    def check_filename_length(self, filename):
        if len(filename) > 59:
            raise ValueError("Input filename must be 59 characters or less")

    @classmethod
    def encrypt_file(cls, input_file, output_file, key_file):
        key = cls.read_key_file(key_file)
        aes = cls(key)
        
        aes.check_filename_length(os.path.basename(input_file))
        aes.validate_key_file(key_file)
        
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        
        ciphertext = aes.encrypt(plaintext, os.path.basename(input_file))
        
        with open(output_file, 'wb') as f:
            f.write(ciphertext)
        
        aes.finalize()

    @classmethod
    def decrypt_file(cls, input_file, key_file):
        key = cls.read_key_file(key_file)
        aes = cls(key)
        
        aes.validate_key_file(key_file)
        
        with open(input_file, 'rb') as f:
            ciphertext = f.read()
        
        plaintext = b''  # Initialize plaintext to avoid UnboundLocalError
        try:
            original_filename, plaintext = aes.decrypt(ciphertext)
            print(f"Decrypted filename: {original_filename}")
            
            output_file = original_filename
            if os.path.exists(output_file):
                output_file = "x_" + output_file
            
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            
            aes.finalize()
            
            return output_file
        except UnicodeDecodeError as e:
            print(f"Error decoding filename: {e}")
            print("Using a default filename for output.")
            output_file = "decrypted_output.bin"
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            return output_file
    
    @staticmethod
    def run_main():
        print("ARGS: ", sys.argv)
        if len(sys.argv) == 4:
            # Encryption mode
            input_file, output_file, key_file = sys.argv[1:]
            Myaesprog.encrypt_file(input_file, output_file, key_file)
            print(f'Encrypted {input_file} to {output_file}')
        elif len(sys.argv) == 3:
            # Decryption mode
            input_file, key_file = sys.argv[1:]
            if not input_file.endswith('.aes'):
                print("Error: Input file for decryption must end with .aes")
                sys.exit(1)
            output_file = Myaesprog.decrypt_file(input_file, key_file)
            print(f'Decrypted {input_file} to {output_file}')
        else:
            print('Usage:')
            print('For encryption: python Myaesprog.py <input_file> <output_file> <key_file>')
            print('For decryption: python Myaesprog.py <input_file> <key_file>')
            sys.exit(1)
        
        print('Done!')

if __name__ == '__main__':
    Myaesprog.run_main()