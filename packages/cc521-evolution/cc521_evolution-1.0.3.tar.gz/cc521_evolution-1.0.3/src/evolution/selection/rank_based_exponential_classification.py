#!/usr/bin/env python3
#
# Implementation of proportional to rank based selection strategy (exponential classification)

import math
import random
import functools
import collections
from typing import Callable

from .misc import FitnessEvaluation
from .base import SelectionStrategy
from ..fitness import Fitness

class RankBasedExponentialClassification(SelectionStrategy):
    """Rank based selection strategy (Exponential Classification)"""
    def __init__(self, fitness: Fitness, 
                 selection_probability: Callable[int, float] = lambda i, c: (1.0-math.exp(-i))/c,
                 population_size: int):
        super(SelectionStrategy, self).__init__(fitness)

        c = sum([1-math.exp(-i) for i in range(1, population_size+1)]) # sum of probability is 1

        self.selection_probability: Callable =  functools.partial(selection_probability, c=c)
        self.population_size = population_size


    def select(self, k: int, individuals: List[Individual]) -> List[Individual]:
        """
        Inputs
            k: number of individuals to select
            individuals: collection of individuals to select from
        
        Ouputs
            k selected individuals
        """
        n = len(individuals)
        probability_func = self.selection_probability

        fitness = [FitnessEvaluation(x, self.fitness(x)) for x in individuals])
        sorted_fitness = sorted(fitness, key=lambda x: x.fitness)

        sorted_individuals = [x.individual for x in sorted_fitness]
        probability = [probability_func(i, s) for i in range(n)]

        return random.choice(sorted_individuals, weights=probability, k=k)

