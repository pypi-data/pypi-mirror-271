#!/usr/bin/env python3
#
# Perform a gray encoding of a gen

import math
import random
import math
from typing import List
from .base import GenEncoder, BitGenEncoder, Gen
from .binary import to_binary, from_binary

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


class GrayGenEncoder(BitGenEncoder):
    def __init__(self, nbits):
        super(GrayGenEncoder, self).__init__(nbits)

    def encode(self, x: object) -> Gen:
        assert isinstance(x, int) or isinstance(x, str)

        if isinstance(x, int):
            return Gen(value = [int(bit) for bit in to_gray(x, self.nbits)])
        else:
            if (size := len(x)) > self.nbits:
                logging.warning(f"Expecting a bitstream with at most {self.nbits} bits, but given one with {size} bits. Taking only {self.nbits} least significant bits")
                x = x[-self.nbits:]
            else:
                x = x.zfill(self.nbits)

            bits = []
            for bit in x:
                assert bit in ['0', '1']
                bits.append(int(bit))
            return Gen(value=bits)

    def decode(self, gen: Gen) -> object:
        bits = ""
        for bit in gen.value:
            assert isinstance(bit, int) and bit in [0, 1]
            bits += str(bit)
        return from_gray(bits)
