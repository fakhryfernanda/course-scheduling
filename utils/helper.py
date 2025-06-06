import numpy as np
from utils import io
from collections import Counter

def locate_value(arr: np.ndarray, value: int) -> tuple[int, int]:
    result = np.argwhere(arr == value)
    return tuple(int(i) for i in result[0]) if result.size > 0 else None

def locate_twin(arr: np.ndarray, value: int) -> tuple[int, int]:
    session = value % 10
    twin_value = value + 1 if session == 1 else value - 1
    res = locate_value(arr, twin_value)
    return res

def get_two_hour_pair(arr, val):
    T, R = arr.shape
    t, r = locate_value(arr, val)

    if t > 0 and arr[t - 1, r] == val:
        return (t - 1, r)
    elif t < T - 1 and arr[t + 1, r] == val:
        return (t + 1, r)
    return None

def safe_swap(arr, val, possible_rows, possible_cols):
    T, R = arr.shape
    rows = possible_rows
    cols = possible_cols
    (t,r) = locate_value(arr, val)

    is_two_hour = Counter(arr.flatten(order='F'))[val] == 2
    if is_two_hour:
        pair_location = get_two_hour_pair(arr, val)

    safe = False
    element_checked = 0
    for col in cols:
        for row in rows:
            element_checked += 1
            if row % 10 == 9:
                continue
  
            if row < T - 1 and arr[row, col] == 0:
                if is_two_hour:
                    if arr[pair_location[0], col] == 0:
                        arr[row, col] = val
                        arr[row + 1, col] = val
                        arr[t, r] = 0
                        arr[t + 1, r] = 0
                        safe = True
                        break
                else:
                    arr[row, col] = val
                    arr[t, r] = 0
                    safe = True
                    break

        if safe:
            break

    if not safe:
        print("rows:", rows)
        print("cols:", cols)
        print("element_checked:", element_checked)
        print("fault:", val)
        io.export_to_txt(arr, "debug", "fault.txt")
        raise Exception("Fault cannot be fixed")
    
    return arr

def are_identical(arr1: np.ndarray, arr2: np.ndarray) -> bool:
    return np.array_equal(arr1, arr2)
