#!/users/perkf/AppData/Local/Programs/Python/Python312/python.exe
import numpy as np
import sys
import math
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
vhex = np.vectorize(hex)

class AESencrypt_ECB(object):
  def __init__(self, key):
    self.__key = np.copy(key)
    self.__cipher = Cipher(algorithms.AES(self.__key), modes.ECB())
    self.__encryptor = self.__cipher.encryptor()
  
  def encrypt_blk(self, data_block):
    return( np.frombuffer(self.__encryptor.update(data_block), np.uint8, -1) )

  def finalize(self):
    self.__encryptor.finalize()
    return

class AESdecrypt_ECB(object):
  def __init__(self, key):
    self.__key = np.copy(key)
    self.__cipher = Cipher(algorithms.AES(self.__key), modes.ECB())
    self.__decryptor = self.__cipher.decryptor()
  
  def decrypt_blk(self, data_block):
    return( np.frombuffer(self.__decryptor.update(data_block), np.uint8, -1) )

  def finalize(self):
    self.__decryptor.finalize()
    return

def write_key_file( key, filename ):
  fd = open(filename, 'wb')
  fd.write( base64.b64encode(key) )
  fd.write( b'\n')
  fd.close()
  return

def read_key_file( filename ):
  fd = open(filename, 'rb')
  key_b = base64.b64decode( fd.read() ); fd.close()
  return( np.frombuffer(key_b, np.uint8, -1) )

##########################
# Here we start our main routine
##########################

# this demonstrates generating a key, writing it to a file
# and reading it from a file.  os.urandom is the best to
# use for cryptographic applications
key_tmp = np.frombuffer(os.urandom(32), np.uint8, -1)
# Look at mykey.txt...it is human readable due to the b64 encoding
write_key_file(key_tmp, 'mykey.txt')
key = read_key_file( 'mykey.txt' )

# here is the key in binary
print(f"key = {vhex(key)}\n")
my_aes_enc = AESencrypt_ECB(key)
my_aes_dec = AESdecrypt_ECB(key)

# Create an array to hold data to encode
# AES block size = 16
blk_sz = 16
x = np.zeros(blk_sz, np.uint8)

# Encrypt and decrypt first data block
for i in range(16): x[i] = 65 + i
print(f"x = {x.tobytes()}")
y = my_aes_enc.encrypt_blk(x)
print(f"y = {vhex(y)}")
xhat = my_aes_dec.decrypt_blk(y)
print(f"xhat = {xhat.tobytes() }\n")

# Encrypt and decrypt second data block
for i in range(16): x[i] = 81 + i
print(f"x = {x.tobytes()}")
y = my_aes_enc.encrypt_blk(x)
print(f"y = {vhex(y)}")
xhat = my_aes_dec.decrypt_blk(y)
print(f"xhat = {xhat.tobytes()}")

# We're done so clean up nicely
my_aes_enc.finalize()
my_aes_dec.finalize()
