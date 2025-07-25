import random
import numpy as np
import logging
from logger.evaluation import logger
from datetime import datetime
from globals import *
from dataclasses import dataclass
from typing import List
from ga.genome import Genome
from ga.crossover_operator import CrossoverOperator
from ga.select_parent import SelectParent
from dataframes.curriculum import Curriculum
from utils import io
from utils.helper import are_identical

@dataclass
class ProblemContext:
    curriculum: Curriculum
    time_slot_indices: List[int]
    room_indices: List[int]

class GeneticAlgorithm:
    def __init__(self, context: ProblemContext, population_size: int, max_generation: int = 10, crossover_rate: float = 0.7, mutation_rate: float = 0.1):
        self.context = context

        assert population_size % 2 == 0, "Population size must be even"
        self.population_size = population_size
        self.max_generation = max_generation
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        self.population: List[Genome] = []
        self.generation = 0

    def initialize_population(self):
        self.population = [
            Genome.from_generator(
                self.context.curriculum,
                self.context.time_slot_indices,
                self.context.room_indices
            )
            for _ in range(self.population_size)
        ]

    def export_population(self):
        for i, genome in enumerate(self.population):
            io.export_to_txt(genome.chromosome, f"population/gen_{self.generation}", f"p_{i+1}.txt")

    def eval(self):
        return [
            genome.count_used_rooms()
            for genome in self.population
        ]
    
    def validate(self):
        return [
            genome.check_constraint()
            for genome in self.population
        ]
    
    def log_evaluation(self, gen: int):
        logger.info(f"Generation: {gen}")
        logger.info(f"{self.eval()}\n")
    
    def select(self) -> List[Genome]:
        return SelectParent(method=SELECTION_METHOD).run(self.population)

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        return CrossoverOperator(random_column_start=RANDOMIZE_CROSSOVER).run(parent1, parent2)

    def evolve(self) -> None:
        next_population = []

        # Selection
        parents = self.select()

        # Crossover
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            p2 = parents[i + 1]
            if random.random() < self.crossover_rate and not are_identical(p1.chromosome, p2.chromosome):
                child1 = self.crossover(p1.chromosome, p2.chromosome)
                child2 = self.crossover(p2.chromosome, p1.chromosome)
                next_population.append(Genome(child1))
                next_population.append(Genome(child2))
            else:
                next_population.extend([Genome(p1.chromosome), Genome(p2.chromosome)])

        # No mutation

        self.population = next_population
        self.generation += 1

    def run(self) -> None:
        self.initialize_population()
        self.export_population()
        if LOG_EVALUATION:
            logger.info(f"{datetime.now()}\n")
            self.log_evaluation(gen=0)

        for gen in range(self.max_generation):
            self.evolve()
            self.export_population()
            if LOG_EVALUATION:
                self.log_evaluation(gen=gen+1)