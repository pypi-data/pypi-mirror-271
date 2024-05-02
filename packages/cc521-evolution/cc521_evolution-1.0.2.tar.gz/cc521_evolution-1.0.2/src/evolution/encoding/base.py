#!/usr/bin/env python3
#
# base classes for perform encoding and decoding of a specific domain

from __future__ import annotations

from collections import namedtuple
from abc import ABC, abstractmethod
from typing import List, Tuple, NamedTuple

class Gen:
    def __init__(self, value: object):
        self.value = value # encoded value by GenEncoder associated with this type of Gen

class GenEncoder(ABC):
    @abstractmethod
    def decode(self, x: Gen) -> object:
        pass

    @abstractmethod
    def encode(self, x: object) -> Gen:
        pass

class ChromosomeComponent:
    def __init__(self, gen: Gen, encoder: GenEncoder):
        self.gen = gen
        self.encoder = encoder

class Chromosome:
    def __init__(self, components: List[ChromosomeComponent]):
        self._components = components

    def chromosome_component(self, k: int) -> ChromosomeComponent:
        assert k < self.ngenes
        return self._components[k]
        
    def component(self, k: int) -> Tuple[Gen, GenEncoder]:
        """Return component k of chromosome"""
        component = self.chromosome_component(k)
        return (component.gen, component.encoder)

    @property
    def chromosome_components(self):
        n = self.ngenes
        return [self.chromosome_component(k) for k in range(n)]

    @property
    def components(self) -> List[Tuple[Gen, GenEncoder]]:
        n = self.ngenes
        return [self.component(k) for k in range(n)]

    @property
    def genes(self) -> List[Gen]:
        return [gen for gen, _ in self.components]

    @property
    def ngenes(self) -> int:
        return len(self._components)

    def decode(self) -> List[object]:
        return [encoder.decode(gen) for gen, encoder in self.components]

    def to_str(self, decode: bool = False) -> str:
        out = None
        if decode:
            out = self.decode()
        else:
            out = [gen.value for gen, _ in self.components]
        return f"{out}"

    def __str__(self):
        return self.to_str(decode=False)


# DEPRECATED CLASS [REPLACED BY Gen class with alelos in {0, 1}]
class BitGenEncoder(GenEncoder):
    def __init__(self, nbits: int):
        self.nbits = nbits


class DomainEncoder(ABC):
    """Encode a domain with an specfic encoding specification (e.g. Interval encoding (domain)  with an specific type of GenEncoder)"""
    def __init__(self, gen_encoders: List[GenEncoder]):
        self.gen_encoders = gen_encoders

    def decode(self, chromosome: Chromosome) -> object:
        return [self.decode_component(component) for component in chromosome.chromosome_components]

    def decode_component(self, component: ChromosomeComponent) -> object:
        pass

    @abstractmethod
    def random(self) -> Chromosome:
        pass
    
