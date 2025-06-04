import random
import numpy as np
from utils.lookup import locate_value, locate_twin

class MutationOperator:
    def __init__(self, method: str = "random_swap"):
        self.method = method

    def run(self, chromosome: np.ndarray) -> np.ndarray:
        if self.method == "random_swap":
            return self.random_swap(chromosome)
        else:
            raise ValueError(f"Unsupported mutation method: {self.method}")
        
    def random_swap(self, chromosome, attempts: int = 1, slots_per_day: int = 10) -> None:
        T, R = chromosome.shape
        mutated = chromosome.copy()

        def get_two_hour_pair(t, r, subject_id):
            if t > 0 and mutated[t - 1, r] == subject_id:
                return t - 1
            elif t < T - 1 and mutated[t + 1, r] == subject_id:
                return t + 1
            return None
        
        def is_same_day(val, new_location):
            if val == 0:
                return False

            (t1, r1) = new_location
            twin_location = locate_twin(chromosome, val)

            if twin_location is None:
                return False

            (t2, r2) = twin_location
            return t1 // 10 == t2 // 10
                
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
                valid = False

                t2 = random.choice(valid_2h_time_indices) if is_2h_course else random.randint(0, T - 1)
                r2 = random.randint(0, R - 1)
                val2 = mutated[t2, r2]

                if is_same_day(val1, (t2, r2)):
                    continue

                if is_same_day(val2, (t1, r1)):
                    continue

                if is_2h_course:
                    t2_pair = get_two_hour_pair(t2, r2, val2) if val2 != 0 else None

                    # Check if t2 and t2_pair are valid for swap
                    if val2 == 0:
                        if t2 < T - 1 and mutated[t2 + 1, r2] == 0:
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
                    break
                else:
                    if (t1, r1) == (t2, r2):
                        continue  # avoid self-swap

                    mutated[t1, r1], mutated[t2, r2] = val2, val1
                    count += 1
                    break

        return mutated
