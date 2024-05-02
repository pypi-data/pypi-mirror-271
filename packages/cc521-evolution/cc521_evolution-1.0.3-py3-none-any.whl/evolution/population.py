#!/usr/bin/env python3
#
# Base Population class

from abc import ABC, abstractmethod
from .encoding.base import DomainEncoder, Gen, Chromosome


class Individual:
    """Encapsulate a chromosome and the encoder that generated it"""
    def __init__(self, chromosome: Chromosome, encoder: DomainEncoder):
        self.encoder = encoder
        self._chromosome = chromosome
    
    @property
    def phenotype(self) -> object:
        #import pdb; pdb.set_trace()
        return self.encoder.decode(self._chromosome)
    
    @property
    def chromosome(self) -> object:
        return self._chromosome

    def __repr__(self) -> str:
        return self._chromosome.to_str()


class Population:
    """Just a group of individuals"""
    def __init__(self, domain_encoder: DomainEncoder, population: int = 10):
        self.individuals = [Individual(domain_encoder.random(), domain_encoder) for _ in range(population)]

    @property
    def size(self):
        return len(self.individuals)

    def __iter__(self):
        for individual in self.individuals:
            yield individual
