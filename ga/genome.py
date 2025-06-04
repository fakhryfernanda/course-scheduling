import random
import numpy as np
from ga import generator
from ga.constraint_checker import ConstraintChecker
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
    
    def count_used_rooms(self) -> int:
        return np.count_nonzero(self.chromosome.any(axis=0))
    
    def check_constraint(self) -> bool:
        return ConstraintChecker(self.chromosome).validate()

    def decode(self) -> np.ndarray:
        return self.chromosome.copy()

    def mutate(self):
        pass

    def mutate(self, attempts: int = 5) -> None:
        T, R = self.chromosome.shape
        mutated = self.chromosome.copy()

        def get_two_hour_pair(t, r, subject_id):
            if t > 0 and mutated[t - 1, r] == subject_id:
                return t - 1
            elif t < T - 1 and mutated[t + 1, r] == subject_id:
                return t + 1
            return None

        valid_2h_time_indices = [t for t in range(T - 1) if (t % 10) <= 8]
        count = 0

        while count < attempts:
            t1, r1 = random.randint(0, T - 1), random.randint(0, R - 1)
            val1 = mutated[t1, r1]
            if val1 == 0:
                continue

            t1_pair = get_two_hour_pair(t1, r1, val1)
            is_2h_course = t1_pair is not None

            for _ in range(10):
                t2 = random.choice(valid_2h_time_indices) if is_2h_course else random.randint(0, T - 1)
                r2 = random.randint(0, R - 1)
                val2 = mutated[t2, r2]

                if is_2h_course:
                    t2_pair = get_two_hour_pair(t2, r2, val2) if val2 != 0 else None

                    # Check if t2 and t2_pair are valid for swap
                    valid = False
                    if val2 == 0:
                        if t2 > 0 and mutated[t2 - 1, r2] == 0:
                            t2_pair = t2 - 1
                            valid = True
                        elif t2 < T - 1 and mutated[t2 + 1, r2] == 0:
                            t2_pair = t2 + 1
                            valid = True
                    elif t2_pair is not None and mutated[t2_pair, r2] == val2:
                        valid = True

                    if not valid:
                        continue

                    # Check for overlapping positions
                    swap_positions = {(t1, r1), (t1_pair, r1), (t2, r2), (t2_pair, r2)}
                    if len(swap_positions) < 4:
                        continue  # positions overlap

                    # Perform 2-hour swap
                    mutated[t1, r1], mutated[t2, r2] = val2, val1
                    mutated[t1_pair, r1], mutated[t2_pair, r2] = val2, val1
                    count += 1
                    print("Swapped index:")
                    print((t1, r1), (t2, r2))
                    break
                else:
                    if (t1, r1) == (t2, r2):
                        continue  # avoid self-swap

                    mutated[t1, r1], mutated[t2, r2] = val2, val1
                    count += 1
                    print("Swapped index:")
                    print((t1, r1), (t2, r2))
                    break

        self.chromosome = mutated