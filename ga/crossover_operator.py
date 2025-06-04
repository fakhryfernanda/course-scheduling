import numpy as np
from collections import Counter
from typing import List

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

        def single_crossover(p1, p2):
            child = list(p1)
            available = Counter(p1)

            for idx in replace_indices:
                available[child[idx]] -= 1

            p2_iter = iter(p2)
            modified = 0
            pointer = start_idx

            while modified < half_len:
                gene = next(p2_iter)
                if available[gene] > 0:
                    child[pointer] = gene
                    available[gene] -= 1
                    modified += 1
                    pointer += 1

            return np.array(child).reshape((T, R), order='F')

        child1 = single_crossover(p1, p2)
        child2 = single_crossover(p2, p1)

        return [child1, child2]
