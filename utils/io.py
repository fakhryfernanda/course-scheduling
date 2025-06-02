import os
import numpy as np

def export_to_txt(arr, folder="solutions", filename="solution.txt"):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Full file path
    filepath = os.path.join(folder, filename)

    # Convert array to string without clipping or wrapping
    with np.printoptions(threshold=np.inf, linewidth=10000):
        arr_str = np.array2string(arr, separator=', ')

    # Write to file
    with open(filepath, 'w') as f:
        f.write(arr_str)

def import_from_txt(folder="output", filename="output.txt"):
    filepath = os.path.join(folder, filename)

    with open(filepath, 'r') as f:
        content = f.read()

    # Convert string back to numpy array
    arr = np.array(eval(content), dtype=np.int16)  # Use eval because it's safe with known input like this
    return arr