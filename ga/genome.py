import numpy as np
from ga import generator
from dataframes.curriculum import Curriculum
from dataframes.course import Course
from typing import List

class Genome:
    def __init__(self, chromosome: np.ndarray):
        self.chromosome = chromosome

    @classmethod
    def from_generator(cls, curriculum: Curriculum, course: Course, time_slot_indices: List, room_indices: List):
        guess = generator.generate_valid_guess(curriculum, course, time_slot_indices, room_indices)
        return cls(guess)

    def decode(self) -> np.ndarray:
        return self.chromosome.copy()

    def mutate(self):
        pass

    def crossover(self, other: "Genome") -> "Genome":
        pass
