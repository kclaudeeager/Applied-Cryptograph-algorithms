#!/usr/local/bin/python3
import numpy as np
import sys
import math
import os

if len(sys.argv) == 1:
  print(f"usage is: {sys.argv[0]} any_text_file")
  sys.exit(0)

# Separate our printout from the command we just typed
print(" ")

#Create a numpy uint8 array and convert it to a python b-string.
#Then convert it back to a numpy array and print it
mydata_np = np.asarray( [i for i in range(256)], np.uint8)
mydata_b = mydata_np.tobytes()
print(f"mydata_b = {mydata_b}\n")
mydata_hex = ' '.join([f'\\x{i:02x}' for i in mydata_b])
print(f"mydata_hex = {mydata_hex}\n")
mydata_np_recon = np.frombuffer(mydata_b, np.uint8, -1)
print(f"mydata_np_recon = {mydata_np_recon}\n")

# Create a np.uint8 array of 1's and 0's and pack it into bits
# Use the pattern 0xa0f3
data = np.asarray([1,0,1,0, 0,0,0,0, 1,1,1,1, 0,0,1,1], np.uint8)
data_packed = np.packbits(data)
data_packed_hex = ' '.join([f'\\x{i:02x}' for i in data_packed])
print(f"data_packed_hex = {data_packed_hex}")
# convert the packed data back to an np.uint8 array and print it
data_recon = np.unpackbits( data_packed )
print(f"data_recon = {data_recon}\n")

#Vectorize the built-in function hex for nice printing, verify the packing
#vhex = np.vectorize(hex)
#print(f"data_packed = {vhex(data_packed)}\n")

# Input a file as a b-string, then convert it to a np.uint8 array
# that permits modification (this is why "np.copy" is mandatory!!!)
# then convert it back to a b-string and output it
fdr = open(sys.argv[1], 'rb')
indat_b = fdr.read() ; fdr.close()
print(f"indat_b = {indat_b}\n")
indat = np.copy( np.frombuffer(indat_b, np.uint8, -1) )
indat_shifted = np.zeros( len(indat), np.uint8 )
indat_shifted[10:] = indat[0:-10]
indat_shifted[0:10] = indat[-10:]
print(f"indat_shifted = {indat_shifted.tobytes()}\n")

# manipulate indat as desired, in this case exclusive or
# the original data with the shifted data.  Then show you can
# recover the orignal data by doing an exclusive or again
indat_xor = np.bitwise_xor( indat, indat_shifted)
print(f"indat_xor = {indat_xor.tobytes()}\n")
indat_xor = np.bitwise_xor( indat_xor, indat_shifted)
print(f"indat_xor = {indat_xor.tobytes()}\n")

# write the data to a file
fdw = open('zzz_trash.txt', 'wb')
fdw.write( indat_xor.tobytes() ); fdw.close()
