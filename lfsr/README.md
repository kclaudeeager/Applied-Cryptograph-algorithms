# LFSR Encryption Process
This document explains the Linear Feedback Shift Register (LFSR) encryption process implemented in the `LFSRCrypto` class.

## LFSR Step Function

The `step` method in the `LFSRCrypto` class performs one LFSR step:

1. Uses the polynomial \(1 + X^{14} + X^{17} + X^{18} + X^{19}\).
2. Represents the current state as a 19-bit integer.
3. Taps the bits at indices 13, 16, 17, and 18 (zero-indexed).
4. Computes the sum of these tapped bits, and its modulo 2 gives the feedback bit.
5. Shifts the state right by one bit, placing the feedback bit at the most significant bit (MSB).
6. Returns the least significant bit (LSB) of the old state as output.

## Byte Generation

The `get_byte` method generates a byte:

1. Calls the `step` method 8 times to generate 8 bits.
2. Stores these bits in a NumPy array.
3. Packs the array into a single byte using `np.packbits`.

## Permutation

The class includes byte-level permutation methods:

1. `permute_byte` applies a fixed permutation to the bits of a byte.
2. `inverse_permute_byte` applies the inverse of this permutation.
3. `permute_encode` and `permute_decode` apply these permutations to entire arrays of bytes.

## XOR Operation

The `fsr_xor` method performs the XOR operation:

1. Generates a key stream by calling `get_byte` for each byte of input data.
2. XORs the input data with this key stream using NumPy's `bitwise_xor`.

## Encryption Process

The `encrypt` method:

1. Applies the permutation to the input data.
2. Performs the XOR operation with the LFSR-generated key stream.

## Decryption Process

The `decrypt` method:

1. Performs the XOR operation with the LFSR-generated key stream.
2. Applies the inverse permutation to recover the original data.

## File Operations

The class includes methods for reading from and writing to files:

1. `readfile` reads binary data from a file into a NumPy array.
2. `writefile` writes a NumPy array of data to a binary file.

## Usage

The script can be run from the command line with the following options:

- `encrypt`: Encrypts an input file and saves the result.
- `decrypt`: Decrypts an input file and saves the result.
- `test_lfsr_period`: Tests and prints the period of the LFSR.

Example usage:
```bash
python lfsr_encryption.py <mode> <input_file> <output_file>
```

Example:
```bash
python lfsr_encryption.py encrypt image2encode.png encoded_png_image.dat
```

Where `<mode>` is one of `encrypt`, `decrypt`, or `test_lfsr_period`.

## Note

The LFSR is initialized with a 19-bit seed (`0x67BD5`). This seed is crucial for both encryption and decryption processes to work correctly.