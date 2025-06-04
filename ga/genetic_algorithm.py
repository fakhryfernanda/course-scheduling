from dataclasses import dataclass
from typing import List
from ga.genome import Genome
from ga.crossover_operator import CrossoverOperator
from dataframes.curriculum import Curriculum
from dataframes.course import Course
from utils import io
import numpy as np

@dataclass
class ProblemContext:
    curriculum: Curriculum
    time_slot_indices: List[int]
    room_indices: List[int]

class GeneticAlgorithm:
    def __init__(self, context: ProblemContext, population_size: int):
        self.context = context
        self.population_size = population_size
        self.population: List[Genome] = []

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
            io.export_to_txt(genome.chromosome, "solutions", f"solution_{i+1}.txt")

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

    def select(self):
        pass

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> List[np.ndarray]:
        crossover_operator = CrossoverOperator(method="random_slice")
        return crossover_operator.run([parent1, parent2])

    def mutate(self):
        pass

    def run(self):
        pass