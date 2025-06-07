import numpy as np
from globals import SLOTS_PER_DAY

class ConstraintChecker:
    def __init__(self, chromosome: np.ndarray, verbose: bool = False):
        self.chromosome = chromosome
        self.verbose = verbose

    def check_class_boundary(self) -> bool:
        T, R = self.chromosome.shape
        for t in range(SLOTS_PER_DAY - 1, T, SLOTS_PER_DAY):
            for r in range(R):
                val = self.chromosome[t, r]
                if val == 0:
                    continue
                if t + 1 < T and self.chromosome[t + 1, r] == val:
                    if self.verbose:
                        print(f"Class boundary violation at time {t} and room {r}: value {val}")
                    return False
        return True

    def check_subject_session_per_day(self) -> bool:
        T, R = self.chromosome.shape
        num_days = T // SLOTS_PER_DAY
        for day in range(num_days):
            start = day * SLOTS_PER_DAY
            end = start + SLOTS_PER_DAY
            for t in range(start, end):
                seen_keys = set()
                for r in range(R):
                    val = self.chromosome[t, r]
                    if val == 0:
                        continue
                    subject_id = str(val)[0]
                    class_number = str(val)[1]
                    key = (subject_id, class_number)
                    if key in seen_keys:
                        if self.verbose:
                            print(f"Multiple sessions of subject {subject_id} class {class_number} on day {day}")
                        return False
                    seen_keys.add(key)
        return True

    def validate(self) -> bool:
        if not self.check_class_boundary():
            if self.verbose:
                print("Constraint failed: Class boundary check")
            return False
        if not self.check_subject_session_per_day():
            if self.verbose:
                print("Constraint failed: Subject session per day check")
            return False
        return True
