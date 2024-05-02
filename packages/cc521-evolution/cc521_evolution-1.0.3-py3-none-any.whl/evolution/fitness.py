#!/usr/bin/env python3
#
# Base class for fitness

from abc import ABC, abstractmethod

from .population import Individual

class Fitness(ABC):
    @abstractmethod
    def compute(self, individual: Individual, *args, **kwargs) -> float:
        pass

    def __call__(self, individual: Individual, *args, **kwargs) -> float:
        return self.compute(individual, *args, **kwargs)
