#!/usr/bin/env python3
#
# Mutation mechanism for gen encoded by BitGenEncoder class
import copy
import random
from .base import MutationStrategy
from ...encoding.binary import BitStreamGen
from ...population import Individual

class BitFlipMutation(MutationStrategy):
    def __init__(self):
        super(BitFlipMutation, self).__init__()

    def mutate(self, parent: Individual) -> Individual:
        chromosome = copy.deepcopy(parent.chromosome)
        for gen in chromosome.genes:
            #assert isinstance(gen, BitStreamGen) # CHECK: DomainEncoder is not creating BitStreamGen genes
            #i = random.randint(0, gen.size-1)
            i = random.randint(0, len(gen.value)-1)
            gen.value[i] = 1 ^ gen.value[i] # 1 xor X - invert value of X to its inverse  (X in [0, 1])

        return Individual(chromosome, encoder=parent.encoder)

