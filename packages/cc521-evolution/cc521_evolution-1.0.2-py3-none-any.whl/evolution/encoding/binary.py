#!/usr/bin/env python3
#
# Perform a binary encoding of a gen

import random
import math
import logging
from typing import List
from .base import BitGenEncoder, Gen

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


class BitStreamGen(Gen):
    def __init__(self, value: List[int]):
        for bit in value:
            assert isintance(bit, int) and bit in [0, 1], f"Bit must be an integer and its value must be 0 or 1, not {bit} (gene: {value})"
        super(BitStreamGen, self).__init__(value)

    @property
    def size(self) -> int:
        return len(self.value)

    def __str__(self) -> str:
        return ''.join(self.value)

class BinaryGenEncoder(BitGenEncoder):
    def __init__(self, nbits: int):
        super(BinaryGenEncoder, self).__init__(nbits)

    def encode(self, x: object) -> BitStreamGen:
        assert isinstance(x, int) or isinstance(x, str), f"Object to be encode must be of type int or str"

        if isinstance(x, int):
            return Gen(value = [int(bit) for bit in to_binary(x, self.nbits)])
        else:
            if (size := len(x)) > self.nbits:
                logging.warning(f"Expecting a bitstream with at most {self.nbits} bits, but given one with {size} bits. Taking only {self.nbits} least significant bits")
                x = x[-self.nbits:]
            else:
                x = x.zfill(self.nbits)
                
            bits = []
            for bit in x:
                assert bit in ['0', '1'], f"Bit must be '0' or '1', and not {bit} (object being encoding: {x})"
                bits.append(int(bit))
            return BitStreamGen(value=bits)

    def decode(self, gen: BitStreamGen) -> object:
        #assert isinstance(gen, BitStreamGen), f"gen is expected to be an instance of BitStreamGen class"
        bits = ''.join([str(x) for x in gen.value])
        #import pdb; pdb.set_trace()
        #for bit in gen.value:
        #    assert isinstance(bit, int) and bit in [0, 1] # this responsability was delegated to BitStreamGen (REMOVE)
        #    bits += str(bit)
        return from_binary(bits)
