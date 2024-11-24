import numpy as np
import sys

class LFSRCrypto:
    def __init__(self, seed):
        self.state = seed
        self.is_fsr_xor_on = True

    def step(self):
        # Perform one LFSR step using the polynomial 1 + X^14 + X^17 + X^18 + X^19
        
        #print(f"State: {self.state:019b}")
        # SUM = X^19 + X^18 + X^17 + X^14
        # convert the state to a string of bits
        state_bits = f"{self.state:019b}"
        # print("Length of state bits: ", len(state_bits))
        tap_sum= int(state_bits[13]) + int(state_bits[16]) + int(state_bits[17]) + int(state_bits[18])
        # print(f"Tap sum: {tap_sum}")
        # compute the new bit by computing the modulo 2 sum of the taps
        feedback = tap_sum % 2
        # get a feedback as the last bit of the state
        out = self.state & 1
        # shift the state to the right by one bit
        self.state >>= 1
        # set the first bit to the new bit
        self.state |= feedback << 18
        return out

    def get_byte(self) -> int:
        byte_array = np.zeros(8, dtype=np.uint8)
        for i in range(8):
            byte_array[i] = self.step()
            
        byte = np.packbits(byte_array)[0]
        # print(f"Generated byte: {byte}")
        # print(f"Generated byte: {byte:08b}")
        return byte

    def permute_byte(self, bit:int) -> int:
        permutation = [2, 6, 3, 5, 1, 8, 4, 7]
        permuted_byte = np.zeros(8, dtype=np.uint8)
        bit_array = np.unpackbits(np.array([bit], dtype=np.uint8))
        for i in range(8):
            permuted_byte[i] = bit_array[permutation[i] - 1]
        return np.packbits(permuted_byte)[0]  
       

    def inverse_permute_byte(self, bit: int) -> int:
        permutation = [5, 1, 3, 7, 4, 2, 8, 6]
        inverse_permuted_bits = np.zeros(8, dtype=np.uint8)
        bit_array = np.unpackbits(np.array([bit], dtype=np.uint8))
        for i in range(8):
            inverse_permuted_bits[i] = bit_array[permutation[i] - 1]
        return np.packbits(inverse_permuted_bits)[0]  

    def permute_encode(self, indata: np.ndarray) -> np.ndarray:
        outdata = np.zeros_like(indata)
        for i in range(len(indata)):
            outdata[i] = self.permute_byte(indata[i])
        return outdata

    def permute_decode(self, indata: np.ndarray) -> np.ndarray:
        outdata = np.zeros_like(indata)
        for i in range(len(indata)):
            outdata[i] = self.inverse_permute_byte(indata[i])
        return outdata

    def fsr_xor(self, indata:np.ndarray) -> np.ndarray:
        if not self.is_fsr_xor_on:
            return indata
        key_stream = np.array([self.get_byte() for _ in range(len(indata))], dtype=np.uint8)
        return np.bitwise_xor(indata, key_stream)

    def turn_off_fsr_xor(self):
        self.is_fsr_xor_on = False

    def encrypt(self, indata: np.ndarray) -> np.ndarray:
        outdata = self.permute_encode(indata)
        outdata = self.fsr_xor(outdata)
        return outdata

    def decrypt(self, indata: np.ndarray) -> np.ndarray:
        outdata = self.fsr_xor(indata)
        outdata = self.permute_decode(outdata)
        return outdata

    def readfile(self, filename: str) -> np.ndarray:
        with open(filename, 'rb') as f:
            return np.frombuffer(f.read(), dtype=np.uint8)

    def writefile(self, filename: str, indata: np.ndarray):
        with open(filename, 'wb') as f:
            f.write(indata.tobytes())
            print(f"Wrote {len(indata)} bytes to {filename}")

def parse_args():
    if len(sys.argv) != 4:
        print("Usage: python lfsr_encryption.py <encrypt/decrypt/test_permutation/test_lfsr_period> <input_file> <output_file>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2], sys.argv[3]

def test_lfsr_period(seed: int):
    lfsr_crypto = LFSRCrypto(seed)
    initial_state = lfsr_crypto.state
    period = 0
    while True:
        lfsr_crypto.step()
        period += 1
        if lfsr_crypto.state == initial_state:
            break
    print(f"LFSR period: {period}")

def main():
    mode, input_file, output_file = parse_args()
    seed = 0x67BD5  # Initial 19-bit key
    # convert the seed to a 19-bit integer
    seed = int(f"{seed:019b}", 2)
    lfsr_crypto = LFSRCrypto(seed)

    if mode == 'encrypt':
        indata = lfsr_crypto.readfile(input_file)
        outdata = lfsr_crypto.encrypt(indata)
        lfsr_crypto.writefile(output_file, outdata)
    elif mode == 'decrypt':
        indata = lfsr_crypto.readfile(input_file)
        outdata = lfsr_crypto.decrypt(indata)
        print(f"Decrypted data: {outdata[:24]}...")
        lfsr_crypto.writefile(output_file, outdata)
    elif mode == 'test_lfsr_period':
        test_lfsr_period(seed)
    else:
        print("Invalid mode. Use 'encrypt', 'decrypt', or 'test_lfsr_period'.")
        sys.exit(1)

if __name__ == "__main__":
    main()