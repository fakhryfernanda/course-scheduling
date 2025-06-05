import numpy as np
from collections import Counter
from typing import List
from utils.helper import locate_value, locate_twin, safe_swap

class CrossoverOperator:
    def __init__(self, method: str = "fixed_slice"):
        self.method = method

    def run(self, parents: List[np.ndarray]) -> List[np.ndarray]:
        assert len(parents) == 2, "Only 2-parent crossover is supported."
        parent1, parent2 = parents

        if self.method == "fixed_slice":
            return [self._fixed_slice(parent1, parent2)]
        elif self.method == "random_slice":
            return self._random_slice(parent1, parent2)
        else:
            raise ValueError(f"Unsupported crossover method: {self.method}")

    def _fixed_slice(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        shape = parent1.shape
        parent1 = parent1.flatten(order='F')
        parent2 = parent2.flatten(order='F')

        half = len(parent1) // 2
        child = list(parent1[:half])

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

            if current_counts[gene] < target_counts[gene]:
                child.append(gene)
                current_counts[gene] += 1

            if len(child) == len(parent1):
                break

        while len(child) < len(parent1):
            child.append(0)

        return np.array(child).reshape(shape, order='F')

    def _random_slice(self, parent1: np.ndarray, parent2: np.ndarray) -> List[np.ndarray]:
        T, R = parent1.shape
        total_len = T * R
        half_len = total_len // 2

        p1 = parent1.flatten(order='F')
        p2 = parent2.flatten(order='F')

        start_col = np.random.choice(R // 2)
        start_idx = start_col * T
        replace_indices = list(range(start_idx, start_idx + half_len))

        def check_class_boundary_fault(arr: np.ndarray, slots_per_day: int = 10) -> List[int]:
            T, R = arr.shape
            fault = []

            for t in range(slots_per_day - 1, T, slots_per_day):
                for r in range(R):
                    val = arr[t, r]
                    if val == 0:
                        continue
                    if t + 1 < T and arr[t + 1, r] == val:
                        fault.append(val)

            return [int(f) for f in fault]

        def fix_class_boundary_fault(arr: np.ndarray):
            fault = check_class_boundary_fault(arr)
            if fault is None:
                return arr
                        
            T,R = arr.shape
            for val in fault:
                (t,r) = locate_value(arr, val)


                cols = list(range(R))
                start = cols.index(r)
                cols = cols[start:] + cols[:start]
                
                arr = safe_swap(arr, val, list(range(T-1)), cols)

            return arr

        def check_multiple_subject_session_fault(arr: np.ndarray, slots_per_day: int = 10):
            T, R = arr.shape
            num_days = T // slots_per_day

            fault = []
            for day in range(num_days):
                start = day * slots_per_day
                end = start + slots_per_day
                for t in range(start, end):
                    seen_keys = set()
                    for r in range(R):
                        val = arr[t, r]
                        if val == 0:
                            continue
                        subject_id = int(val) // 100
                        class_number = (int(val) // 10) % 10
                        key = (subject_id, class_number)
                        if key in seen_keys:
                            fault.append(int(val))
                        seen_keys.add(key)
            
            return fault
        
        def fix_multiple_subject_session_fault(arr: np.ndarray):
            fault = check_multiple_subject_session_fault(arr)
            if fault is None:
                return arr
                                    
            T, R = arr.shape
            for val in fault:
                (t,r) = locate_twin(arr, val)
                rows = [i for i in range(T) if i // 10 != t // 10]
                cols = list(range(R))

                arr = safe_swap(arr, val, rows, cols)

            return arr

        def single_crossover(p1, p2):
            child = list(p1)
            original_counter = Counter(child)
            child_counter = Counter(child)

            for idx in replace_indices:
                child_counter[child[idx]] -= 1

            p2_iter = iter(p2)
            modified = 0
            pointer = start_idx

            while modified < half_len:
                gene = next(p2_iter)

                if child_counter[gene] < original_counter[gene]:
                    child[pointer] = gene
                    child_counter[gene] += 1
                    modified += 1
                    pointer += 1

            return np.array(child).reshape((T, R), order='F')


        child1 = single_crossover(p1, p2)
        child1 = fix_class_boundary_fault(child1)
        child1 = fix_multiple_subject_session_fault(child1)

        child2 = single_crossover(p2, p1)
        child2 = fix_class_boundary_fault(child2)
        child2 = fix_multiple_subject_session_fault(child2)

        return [child1, child2]
