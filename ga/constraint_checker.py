import numpy as np

class ConstraintChecker:
    def __init__(self, chromosome: np.ndarray, slots_per_day: int = 10):
        self.chromosome = chromosome
        self.slots_per_day = slots_per_day

    def check_class_boundary(self) -> bool:
        T, R = self.chromosome.shape
        for t in range(self.slots_per_day - 1, T, self.slots_per_day):
            for r in range(R):
                val = self.chromosome[t, r]
                if val == 0:
                    continue
                if t + 1 < T and self.chromosome[t + 1, r] == val:
                    return False
        return True

    def check_subject_session_per_day(self) -> bool:
        T, R = self.chromosome.shape
        num_days = T // self.slots_per_day
        for day in range(num_days):
            start = day * self.slots_per_day
            end = start + self.slots_per_day
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
                        return False
                    seen_keys.add(key)
        return True

    def validate(self) -> bool:
        return all([
            self.check_class_boundary(),
            self.check_subject_session_per_day()
        ])
