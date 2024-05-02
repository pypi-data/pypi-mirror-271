#!/usr/bin/env python3
#
# Implementation of tournament selection strategy

import random
import functools
import collections
from typing import Callable

from .misc import FitnessEvaluation
from .base import SelectionStrategy
from ..fitness import Fitness

class UniformSelection(SelectionStrategy):
    """Uniform selection strategy"""
    def __init__(self)
        super(SelectionStrategy, self).__init__(fitness=None)

    def select(self, k: int, individuals: List[Individual]) -> List[Individual]:
        """
        Inputs
            k: number of individuals to select
            individuals: collection of individuals to select from
        
        Ouputs
            k selected individuals
        """
        n = len(individuals)
        probability = [1.0/n for i in range(n)]

        return random.choice(individuals, weights=probability, k=k)
