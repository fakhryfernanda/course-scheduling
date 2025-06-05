import numpy as np

def locate_value(arr: np.ndarray, value: int) -> tuple[int, int]:
    result = np.argwhere(arr == value)
    return tuple(int(i) for i in result[0]) if result.size > 0 else None

def locate_twin(arr: np.ndarray, value: int) -> tuple[int, int]:
    session = value % 10
    twin_value = value + 1 if session == 1 else value - 1
    res = locate_value(arr, twin_value)
    return res
