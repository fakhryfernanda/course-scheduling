import numpy as np
from ga import generator
from ga.constraint_checker import ConstraintChecker
from ga.mutation_operator import MutationOperator
from dataframes.curriculum import Curriculum
from typing import List

class Genome:
    def __init__(self, chromosome: np.ndarray):
        self.chromosome = chromosome

    @classmethod
    def from_generator(cls, curriculum: Curriculum, time_slot_indices: List, room_indices: List):
        guess = generator.generate_valid_guess(curriculum, time_slot_indices, room_indices)
        return cls(guess)
    
    def count_used_rooms(self) -> int:
        if self.check_constraint():
            count = np.count_nonzero(self.chromosome.any(axis=0))
        else:
            count = 1000
        
        return count 
    
    def check_constraint(self, verbose: bool = False) -> bool:
        return ConstraintChecker(self.chromosome, verbose=verbose).validate()

    def decode(self) -> np.ndarray:
        return self.chromosome.copy()
    
    def mutate(self) -> None:
        self.chromosome = MutationOperator(method="random_swap").run(self.chromosome)