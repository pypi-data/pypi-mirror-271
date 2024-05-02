#!/usr/bin/env python3
#
# Perform encoding of an interval

import random
import math
from typing import List
from .base import DomainEncoder, GenEncoder, BitGenEncoder
from .base import Chromosome, ChromosomeComponent, Gen

class IntervalPartition:
    def __init__(self, a:float, b: float, delta: float, gen_encoder_cls: type[GenEncoder]):
        self.lower_bound = a
        self.upper_bound = b
        self.delta = delta
        self.gen_encoder_cls = gen_encoder_cls

    def __str__(self):
        return {'lower_bound': self.lower_bound,
                'upper_bound': self.upper_bound,
                'delta': self.delta,
                'gen_encoder_cls': self.gen_encoder_cls}


class IntervalEncoder(DomainEncoder):
    def __init__(self, partition: IntervalPartition):
        """Initialize BinaryEncodingInterval to encode partition generate by delta on interval [a, b]"""
        self._partition = partition

        a = partition.lower_bound
        b = partition.upper_bound
        delta = partition.delta
        gen_encoder_cls = partition.gen_encoder_cls

        if b <= a:
            raise Exception(f"Expected a regular interval (low-bound: {a}, high-bound: {b})")

        self.lower_bound = a
        self.upper_bound = b
        self.nbits = math.ceil(math.log2((b-a)/delta)) # estimate numbers of bits to represent partition
        self.delta = (b-a)/(2**self.nbits-1)
        
        assert issubclass(gen_encoder_cls, BitGenEncoder)
        super(IntervalEncoder, self).__init__(gen_encoders = [gen_encoder_cls(nbits=self.nbits)])

    def _phenotype(self, jumps: int) -> float:
        """
        Inputs
        ======
        jumps: number of jumps from first encoded value (lower bound of interval)
        """
        return self.lower_bound + jumps*self.delta

    def decode(self, chromosome: Chromosome) -> float:
        """decode chromosome from encoded form to phenotype"""
        assert chromosome.ngenes == 1, f"Expecting a chomosome with one gen, supplied chomosome with {chromosome.ngenes} genes"
        import pdb; pdb.set_trace()
        phenotype = super().decode(chromosome)[0]
        return phenotype

    def decode_component(self, component: ChromosomeComponent) -> float:
        """decode chromosome component from encoded form to phenotype"""
        gen, encoder = component.gen, component.encoder
        #import pdb; pdb.set_trace()
        jumps = encoder.decode(gen) # jumps from 0000 ... 000  chromosome to supplied chromosome 
        return self._phenotype(jumps)

    @property
    def gen_encoder(self):
        return self.gen_encoders[0]

    @property
    def describe(self):
        x = self._partition
        x['delta'] = self.delta # updated delta
        x['bits'] = self.nbits
        return x

    def random(self) -> Chromosome:
        """
        Generate a point on encoded interval

        Returns
        =======
        chromosome
        """
        components = []
        for gen_encoder in self.gen_encoders:
            point = random.randint(0, 2**self.nbits-1)
            gen = gen_encoder.encode(point)
            component = ChromosomeComponent(gen, encoder=gen_encoder)
            components.append(component)

        return Chromosome(components=components)


class MultipleIntervalEncoder(DomainEncoder):
    def __init__(self, partitions: List[IntervalPartition]):
        self.interval_encoders: List[IntervalEncoder] = [IntervalEncoder(partition=p) for p in partitions]

    def encoder(self, k: int) -> IntervalEncoder:
        assert k >= len(self.interval_encoder), f"Number of interval encoders: {len(self.interval_encoder)} - Trying to acces to {k}"
        return self.interval_encoder[k]

    @property
    def describe(self):
        return [encoder.describe for encoder in self.interval_encoders]

    def decode(self, chromosome: Chromosome) -> List[float]:
        assert len(self.interval_encoders) == chromosome.ngenes, f"Expecting a chromosome with {len(self.interval_encoders)} genes, not one with {chromosome.ngenes}."

        #import pdb; pdb.set_trace()
        phenotype = [encoder.decode_component(component) 
                     for encoder, component in zip(self.interval_encoders, chromosome.chromosome_components)]

        return phenotype

    def random(self) -> Chromosome:
        """
        Generate a point on encoded interval

        Returns
        =======
        chromosome: Chromosome
        """
        
        components = []
        for encoder in self.interval_encoders:
            chromosome = encoder.random() # generated interval chromosome has only 1 component
            component = chromosome.chromosome_component(0)
            components.append(component)

        return Chromosome(components=components)
