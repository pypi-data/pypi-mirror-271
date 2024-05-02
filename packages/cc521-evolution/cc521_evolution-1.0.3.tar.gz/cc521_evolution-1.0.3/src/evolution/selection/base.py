#!/usr/bin/env python3
#
# Base class for selection strategies

from typing import List
from abc import ABC, abstractmethod

from ..population import Individual
from ..fitness import Fitness

class SelectionStrategy(ABC):
    def __init__(self, fitness: Fitness):
        self.fitness = fitness

    @abstractmethod
    def select(self, k:int, individuals: List[Individual], *args, **kwargs) -> List[Individual]:
        """Select k individuals from a collection of them"""
        pass
