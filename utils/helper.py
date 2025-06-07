import numpy as np
from utils import io
from globals import SLOTS_PER_DAY
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

    arr2 = arr.copy()
    arr2[t, r] = 0

    return locate_value(arr2, val)

def safe_swap(arr, val, possible_rows, possible_cols):
    try:
        T, R = arr.shape
        rows = possible_rows
        cols = possible_cols
        t, r = locate_value(arr, val)

        is_two_hour = Counter(arr.flatten())[val] == 2
        pair_location = get_two_hour_pair(arr, val) if is_two_hour else None

        safe = False
        for col in cols:
            for row in rows:
                if (row + 1) % SLOTS_PER_DAY == 0:
                    continue

                if arr[row, col] != 0:
                    continue
            
                if is_two_hour:
                    t_pair, r_pair = pair_location
                    diff = t_pair - t
                    if diff == T - 1:
                        diff = -1

                    if diff == -1 and row == 0:
                        continue

                    if arr[row + diff, col] == 0:
                        arr[row, col] = val
                        arr[row + diff, col] = val

                        arr[t, r] = 0
                        arr[t_pair, r] = 0
                        safe = True
                        break
                else:
                    arr[row, col] = val
                    arr[t, r] = 0
                    safe = True
                    break

            if safe:
                break

    except:
        io.export_to_txt(arr, "debug", f"fault.txt")
        print("val:", val)
        print("diff:", diff)
        raise Exception("Safe swap error")

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
