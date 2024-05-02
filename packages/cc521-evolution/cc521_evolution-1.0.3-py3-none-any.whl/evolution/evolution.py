#!/usr/bin/env python3
#
# Base Generatic Evolutionary Algorithm Class
from __future__ import annotations

from tqdm import tqdm
import uuid
import random
import logging
import json
from abc import abstractmethod
from typing import Callable, Concatenate, List

from .population import Population, Individual
from .selection.misc import FitnessEvaluation
from .selection.base import SelectionStrategy
from .variation.crossover.base import CrossoverStrategy
from .variation.mutation.base import MutationStrategy

class Evolution:
    def __init__(self, population: Population, *,
                 fitness: Callable[[object], float],
                 selection_strategy: SelectionStrategy,
                 # variation strategies
                 crossover_strategy: CrossoverStrategy, 
                 mutation_strategy: MutationStrategy, 
                 crossover_prob: float = 0.7, mutation_prob: float = 0.2):
        self.fitness_func = fitness
        self.population = population
        self.generation = 1

        self.best: Individual = None # invidividual with the largest fitness value on the last generation
        self.worse: Individual = None # invidividual with the smallest fitness value on the last generation

        self.selection_strategy = selection_strategy

        self.crossover_strategy = crossover_strategy
        self.crossover_prob = crossover_prob

        self.mutation_strategy = mutation_strategy
        self.mutation_prob = mutation_prob

        self.logger: logging.Logger = logging.getLogger(type[self].__name__)

    def select(self, k: int) -> List[Individual]:
        """ Select k individual from the current population using a selection strategy"""
        return self.selection(k, self.population.individuals)

    def selection(self, k: int, individuals: List[Individual], *args, **kwargs) -> List[Individual]:
        """ Select top k individual using an a selection strategy"""
        return self.selection_strategy.select(k, self.population.individuals)

    def variation(self, k: int, parents: List[Individual]) -> List[Individual]:
        """Perform variation operators (reproduction mechanism) on a group of selected individual
        to generate the k individuals"""

        count = 0
        generated_individuals = []
        while count < k:
            r = random.random()
            if self.crossover_prob > r:
                parent1 = random.choice(parents)
                parent2 = random.choice(parents) # check that the two parent are different individuals

                children = self.crossover_strategy.crossover(parent1, parent2)
                generated_individuals += children
                count += len(children)

            if self.mutation_prob > r and count < k-1:
                parent = random.choice(parents)
                child = self.mutation_strategy.mutate(parent)
                generated_individuals.append(child)
                count += 1

        return generated_individuals


    def converged(self) -> bool:
        """
        Function that determine if the current population of the evolution satisfice the required condition
        using an evaluation function

        True means that the evoluation process has converged and the evolution must be stoped, 
            otherwise the evoltion process will continue
        """
        return False # if the problen hasn't a well defined stop condition, just return False

    def evaluate(self, individuals: List[Individual]) -> dict:
        n = len(individuals)
        fitnessEvaluation = [FitnessEvaluation(x, self.fitness_func(x)) for x in individuals]

        avg_fitness = sum([x.fitness for x in fitnessEvaluation]) / float(n)
        best = max(fitnessEvaluation, key=lambda t: t.fitness)
        worse = min(fitnessEvaluation, key=lambda t: t.fitness)

        self.best = best.individual
        self.worse = worse.individual

        return {'generation': self.generation, 
                'fitness': {
                    'average': avg_fitness, 'best': best.fitness, 'worse': worse.fitness
                    },
                'individual': {
                    'best': [gen.value for gen in best.individual.chromosome.genes],
                    'worse': [gen.value for gen in worse.individual.chromosome.genes]
                    }
                }

    def population_fitness(self) -> List[float]:
        """Compute the fitness of the current population"""
        return [self.fitness_func(individual) for individual in self.population]

    def _evolve(self, max_generations: int, 
                  selection: int, descendents: int, *args, **kwargs) -> Population:
        """
        perform the evolution of initial population using multiple variation operations
        this method quits when max number of iteratons were done or the convergence condition was met

        Inputs
        =======
        max_generations: maximun number of iterations (or generations - evolutions)
        selection: number of parents selected fom current population (for generate next generation)
        descendents: number of descendents to generate using variation operation over selected individuals

        Output
        ======
        evolved population
        """
        pass
    

    def evolve(self, max_generations: int, 
                  selection: int, descendents: int, *args, **kwargs) -> Population:
        """
        perform the evolution of initial population using multiple variation operations
        this method quits when max number of iteratons were done or the convergence condition was met

        Inputs
        =======
        max_generations: maximun number of iterations (or generations - evolutions)
        selection: number of parents selected fom current population (for generate next generation)
        descendents: number of descendents to generate using variation operation over selected individuals

        Output
        ======
        evolved population
        """
        
        population_size = self.population.size # population size

         
        with tqdm(total=max_generations) as pbar: # progress bar
            while self.generation < max_generations and not self.converged():
                #import pdb; pdb.set_trace()
                population = self.population.individuals # current generation

                selected = self.select(selection) # select individuals from current generation for reproduction

                generated = self.variation(descendents, selected + population) # reproduction (crossover + mutation)
                population = self.selection(population_size, generated + population) # select individuals for next generation 

                self.population.individuals = population # replace old generation with new on
                self.generation += 1
                
                pbar.update(1)
                # compute metric of current generation (next-generation)
                evaluation = self.evaluate(self.population.individuals)
                pbar.set_postfix({'generation': self.generation, **evaluation['fitness']})

        if self.converged():
            print("The evolution process was converged")   

        # best is element with the largest fitness and worse is the element with the smallest fitness
        # Therefore when is maximization problem our objective is find the individual that has the best fitness (the best)
        #, but in minimization problems our objective is find the individual with the lowerst fitness (the worse)
        print("\n" + "="*20)
        print(f"Best: {self.best.phenotype}")
        print(f"Worse: {self.worse.phenotype}")
        print("="*20)

        file = f"evolution-{uuid.uuid4().hex}.json"
        print(f"Writing results to: {file}")
        with open(file, 'w') as f:
            json.dump(evaluation, f, indent=4)
