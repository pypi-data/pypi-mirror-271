#!/usr/bin/env python3
#
# Crossover strategy ovet BitStreamGen genes

from abc import abstractmethod
import copy
import random
from typing import Tuple
from .base import CrossoverStrategy
from ...encoding.binary import BitStreamGen
from ...population import Individual


class OnePointCrossover(CrossoverStrategy):
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        chromosome1 = copy.deepcopy(parent1.chromosome)
        chromosome2 = copy.deepcopy(parent2.chromosome)

        assert chromosome1.ngenes == chromosome2.ngenes

        for gene1, gene2 in zip(chromosome1.genes, chromosome2.genes):
            #assert isinstance(gene1, BitStreamGen) and isinstance(gene2, BitStreamGen), \
            #        f"Genes {gene1} and {gene2} must be instances of BitStreamGen class"
            #assert gene1.size == gene2.size, \
            assert len(gene1.value) == len(gene2.value), \
                    f"Genes must have the same size for crossover operation, received gene1.size={gene1.size} and gene2.size={gene2.size}"

            #i = random.randint(0, gene1.size-1)
            i = random.randint(0, len(gene1.value)-1)

            tmp = gene2.value[i:]
            gene2.value[i:] = gene1.value[i:]
            gene1.value[i:] = tmp
            #import pdb; pdb.set_trace()
 
        return (Individual(chromosome1, encoder=parent1.encoder),
                Individual(chromosome2, encoder=parent2.encoder))
