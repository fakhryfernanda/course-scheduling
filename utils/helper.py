import numpy as np

def locate_value(arr: np.ndarray, value: int) -> tuple[int, int]:
    result = np.argwhere(arr == value)
    return tuple(int(i) for i in result[0]) if result.size > 0 else None

def locate_twin(arr: np.ndarray, value: int) -> tuple[int, int]:
    session = value % 10
    twin_value = value + 1 if session == 1 else value - 1
    res = locate_value(arr, twin_value)
    return res

def safe_swap(arr, val, possible_rows, possible_cols):
    T, R = arr.shape
    rows = possible_rows
    cols = possible_cols
    (t,r) = locate_value(arr, val)

    safe = False
    for col in cols:
        for row in rows:
            if row % 10 == 9:
                continue

            if t < T - 1 and arr[row,col] == 0 and arr[row+1,col] == 0:
                arr[row,col] = val
                arr[row+1,col] = val
                arr[t,r] = 0
                arr[t+1,r] = 0
                safe = True
                break
        if safe:
            break

    if not safe:
        raise Exception("Fault cannot be fixed")
    
    return arr
