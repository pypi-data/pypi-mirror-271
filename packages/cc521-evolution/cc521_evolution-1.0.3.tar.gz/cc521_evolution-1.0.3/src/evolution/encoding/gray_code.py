#!/usr/bin/env python3
import math


def to_binary(number: int, nbits: int = None) -> str:
	"""From decimal to binary (with an specific number of bits)"""
	if nbits is None:
		nbits = math.ceil(math.log2(number)) if number > 0 else 0
		
	binary = bin(number)[2:]
	binary = binary.zfill(nbits)

	return binary

def from_binary(binary: str) -> int:
	"""From binary to decimal"""
	return int(binary, 2)

def binary_to_gray(binary: str) -> str:
	gray = [binary[0]]  # Initialize with MSB of binary
	for i in range(1, len(binary)):
		# XOR operation to get Gray code bit
		gray_bit = str(int(binary[i-1]) ^ int(binary[i]))
		gray.append(gray_bit)
	return ''.join(gray)
	
def gray_to_binary(gray: str) -> str:
    binary = [gray[0]]  # Initialize with MSB of Gray code
    for i in range(1, len(gray)):
        # XOR operation to get the binary bit
        binary_bit = str(int(gray[i]) ^ int(binary[i-1])) # bk = gk XOR b_{k+1}
        binary.append(binary_bit)
    return ''.join(binary)

def to_gray(number: int, nbits: int = None) -> str:
	binary = to_binary(number, nbits)
	return binary_to_gray(binary)
	
def from_gray(gray: str) -> int:
	binary = gray_to_binary(gray)
	return from_binary(binary)
	
if __name__=="__main__":
	n = 17
	
	print("[DEFAULT BITS] ", n, to_binary(n), from_binary(to_binary(n)))
	print("[WITH 8 BITS] ", n, to_binary(n, nbits=8), from_binary(to_binary(n, nbits=8)))
	
	print("==================")
	for n in range(0, 16):
		print(n, to_binary(n), to_gray(n), from_gray(to_gray(n)))
