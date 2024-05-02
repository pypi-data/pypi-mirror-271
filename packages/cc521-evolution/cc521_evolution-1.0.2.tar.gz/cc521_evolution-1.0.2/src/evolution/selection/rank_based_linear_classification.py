#!/usr/bin/env python3
#
# Implementation of proportional to rank based selection strategy

import random
import functools
import collections
from typing import Callable

from .misc import FitnessEvaluation
from .base import SelectionStrategy
from ..fitness import Fitness

class RankBasedLinearClassification(SelectionStrategy):
    """Rank based selection strategy (Linear Classification)"""
    def __init__(self, fitness: Fitness, 
                 selection_probability: Callable[[int, float], float] = lambda i, s, u: (2.0-s)/u + 2.0*i*(s-1)/(u*(u-1))):
        super(SelectionStrategy, self).__init__(fitness)
        self.selection_probability: Callable = selection_probability

    def select(self, k: int, individuals: List[Individual], s: float = 1.5) -> List[Individual]:
        """
        Inputs
            k: number of individuals to select
            individuals: collection of individuals to select from
            s: parameter of selection probability function (best individual advantage)
        
        Ouputs
            k selected individuals
        """
        n = len(individuals)
        probability_func = functools.partial(self.selection_probability, u=n)

        fitness = [FitnessEvaluation(x, self.fitness(x)) for x in individuals])
        sorted_fitness = sorted(fitness, key=lambda t: t.fitness)

        sorted_individuals = [x.individual for x in sorted_fitness]
        probability = [probability_func(i, s) for i in range(n)]

        return random.choice(sorted_individuals, weights=probability, k=k)

