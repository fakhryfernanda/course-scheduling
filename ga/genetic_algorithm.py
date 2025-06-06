import random
import numpy as np
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
    
    def select(self) -> List[Genome]:
        return SelectParent(method="tournament").run(self.population)

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> List[np.ndarray]:
        crossover_operator = CrossoverOperator(method="random_slice")
        return crossover_operator.run([parent1, parent2])

    def mutate(self):
        pass

    def evolve(self):
        next_population = []

        # Selection
        parents = self.select()

        # Crossover
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            p2 = parents[i + 1]
            if random.random() < self.crossover_rate and not are_identical(p1.chromosome, p2.chromosome):
                children_chromosomes = self.crossover(p1.chromosome, p2.chromosome)
                next_population.extend([Genome(chromosome) for chromosome in children_chromosomes])
            else:
                next_population.extend([Genome(p1.chromosome), Genome(p2.chromosome)])

        # Mutation
        for genome in next_population:
            if random.random() < self.mutation_rate:
                genome.mutate()

        self.population = next_population

    def run(self):
        self.initialize_population()
        print("Generation 0")
        print(self.eval(), end="\n\n")

        for gen in range(self.max_generation):
            print(f"Generation {gen+1}")
            self.evolve()
            self.export_population()
            print(self.eval(), end="\n\n")