#!/usr/bin/env python3
#
# base class for mutation operations

from abc import ABC, abstractmethod
from ...population import Individual

class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self, parent: Individual) -> Individual:
        pass
