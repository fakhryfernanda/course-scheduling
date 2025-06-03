from dataclasses import dataclass
from typing import List
from ga.genome import Genome
from dataframes.curriculum import Curriculum
from dataframes.course import Course
from utils import io
from collections import Counter
import numpy as np

@dataclass
class ProblemContext:
    curriculum: Curriculum
    courses: Course
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
                self.context.courses,
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

    def crossover_old(self, parent1: np.ndarray, parent2: np.ndarray):
        shape = parent1.shape

        parent1 = parent1.flatten(order='F')
        parent2 = parent2.flatten(order='F')

        half = len(parent1) // 2
        child = list(parent1[:half])

        # Count target gene frequencies from both parents
        target_counts = Counter(parent1)
        current_counts = Counter(child)

        n_zeros = target_counts[0]
        zeros_in_child = current_counts[0]

        for gene in parent2:
            if gene == 0:
                if zeros_in_child < n_zeros:
                    child.append(0)
                    zeros_in_child += 1
                continue

            # Allow duplicates up to how often they appear in parent1
            if current_counts[gene] < target_counts[gene]:
                child.append(gene)
                current_counts[gene] += 1

            if len(child) == len(parent1):
                break

        # Padding in case something went wrong (e.g., insufficient gene diversity)
        while len(child) < len(parent1):
            child.append(0)

        return np.array(child).reshape(shape, order='F')
    
    def crossover(self, parent1: np.ndarray, parent2: np.ndarray):
        T, R = parent1.shape
        total_len = T * R
        half_len = total_len // 2

        # Flatten both parents
        p1 = parent1.flatten(order='F')
        p2 = parent2.flatten(order='F')

        # Shared random starting column
        start_col = np.random.choice(R // 2)
        start_idx = start_col * T
        replace_indices = list(range(start_idx, start_idx + half_len))

        def single_crossover(source, donor):
            child = list(source)
            available = Counter(source)

            # Remove counts of genes in the slice
            for idx in replace_indices:
                available[child[idx]] -= 1

            donor_iter = iter(donor)
            modified = 0
            ptr = start_idx

            while modified < half_len:
                gene = next(donor_iter)
                if available[gene] > 0:
                    child[ptr] = gene
                    available[gene] -= 1
                    modified += 1
                    ptr += 1

            return np.array(child).reshape((T, R), order='F')

        child1 = single_crossover(p1, p2)
        child2 = single_crossover(p2, p1)

        return child1, child2


    def mutate(self):
        pass

    def run(self):
        pass