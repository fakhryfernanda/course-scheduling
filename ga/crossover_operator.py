import numpy as np
import logging
from utils import logger
from globals import *
from collections import Counter
from utils.helper import locate_value, locate_twin, safe_swap

class CrossoverOperator:
    def __init__(self, random_column_start: bool = False):
        self.random_column_start = random_column_start

    def run(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        child = self.single_crossover(parent1, parent2)
        child = self.fix_class_boundary_fault(child)
        child = self.fix_multiple_subject_session_fault(child)

        return child
        
    def single_crossover(self, p1: np.ndarray, p2: np.ndarray):
        T, R = p1.shape
        if self.random_column_start:
            start_col = np.random.choice(R // 2 + 1)
        else:
            start_col = R // 2
        logging.info(f"Crossover with starting column: {start_col}")

        p1 = p1.flatten(order='F')
        p2 = p2.flatten(order='F')

        start_index = start_col * T

        half_len = (T * R) // 2
        replace_indices = list(range(start_index, start_index + half_len))

        child = list(p1)
        original_counter = Counter(child)
        child_counter = Counter(child)

        existed_zeros = sum(1 for i in range(start_index) if p1[i] == 0)
        met_zeros = 0

        for idx in replace_indices:
            child_counter[child[idx]] -= 1

        p2_iter = iter(p2)
        modified = 0
        pointer = start_index

        while modified < half_len:
            try:
                gene = next(p2_iter)
            except:
                raise Exception("p2_iter exhausted before child is filled.")

            if child_counter[gene] < original_counter[gene]:
                if gene == 0 and met_zeros < existed_zeros:
                    met_zeros += 1
                    continue

                child[pointer] = gene
                child_counter[gene] += 1
                modified += 1
                pointer += 1

        return np.array(child).reshape((T, R), order='F')
    
    def fix_class_boundary_fault(self, arr: np.ndarray):
        T, R = arr.shape
        fault = []

        for t in range(SLOTS_PER_DAY - 1, T, SLOTS_PER_DAY):
            for r in range(R):
                val = arr[t, r]
                if val == 0:
                    continue
                if t + 1 < T and arr[t + 1, r] == val:
                    fault.append(int(val))

        if fault is None:
            return arr
                    
        for val in fault:
            (t,r) = locate_value(arr, val)

            rows = list(range(T-1))
            cols = list(range(R))
            start = cols.index(r)
            cols = cols[start:] + cols[:start]
            
            arr = safe_swap(arr, val, rows, cols)

        return arr
        
    def fix_multiple_subject_session_fault(self, arr: np.ndarray):
        T, R = arr.shape
        num_days = T // SLOTS_PER_DAY

        fault = []
        for day in range(num_days):
            start = day * SLOTS_PER_DAY
            end = start + SLOTS_PER_DAY
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
        
        if fault is None:
            return arr
                                
        for val in fault:
            (t,r) = locate_twin(arr, val)
            rows = [i for i in range(T) if i // 10 != t // 10]
            cols = list(range(R))

            arr = safe_swap(arr, val, rows, cols)

        return arr
