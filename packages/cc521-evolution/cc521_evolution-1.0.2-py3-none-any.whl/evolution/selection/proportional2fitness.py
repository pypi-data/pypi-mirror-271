#!/usr/bin/env python3
#
# Implementation of proportional to fitness selection strategy

import random
from typing import List

from .base import SelectionStrategy
from ..fitness import Fitness
from ..population import Individual

class ProportionalToFitness(SelectionStrategy):
    """ Proportional to fitness selection strategy"""
    def __init__(self, fitness: Fitness):
        super(ProportionalToFitness, self).__init__(fitness)

    def select(self, k: int, individuals: List[Individual]) -> List[Individual]:
        n = len(individuals)
        total_fitness = sum([self.fitness(x) for x in individuals])

        probability = [self.fitness(x)/total_fitness for x in individuals]

        return random.choices(individuals, weights=probability, k=k)

