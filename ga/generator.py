import numpy as np
from typing import List
from dataframes.curriculum import Curriculum

def generate_valid_guess(curriculum: Curriculum, time_slot_indices: List, room_indices: List):
    """
    Generate a valid solution using your 1D approach with transpose.
    Parameters:
    - curriculum (Curriculum): Curriculum object with session info
    - course (Course): Course object containing durations
    - time_slot_indices (List): Time slots available
    - room_indices (List): Room indices available

    Returns:
    - np.ndarray shape (T, R)
    """
    T = len(time_slot_indices)
    R = len(room_indices)

    room_indices = [i for i in range(R)]
    np.random.shuffle(room_indices)

    total_durations = (curriculum.df["classes"] * (curriculum.df["session_1"] + curriculum.df["session_2"])).sum()
    total_slots = T * R
    
    if total_durations > total_slots:
        raise ValueError("Not enough slots for all courses")

    arr_2d = np.full((T, R), fill_value=0, dtype=np.int16)

    # Session 1
    c12 = curriculum.get_classes_map(session=1, duration=2)
    arr_2d = place_parallel_classes(arr_2d, T, R, class_dict=c12, code=(1,2))

    c11 = curriculum.get_classes_map(session=1, duration=1)
    arr_2d = place_parallel_classes(arr_2d, T, R, class_dict=c11, code=(1,1))

    # Session 2
    c22 = curriculum.get_classes_map(session=2, duration=2)
    arr_2d = place_parallel_classes(arr_2d, T, R, class_dict=c22, code=(2,2))

    c21 = curriculum.get_classes_map(session=2, duration=1)
    arr_2d = place_parallel_classes(arr_2d, T, R, class_dict=c21, code=(2,1))

    return arr_2d

def place_parallel_classes(arr_2d: np.ndarray, T: int, R: int, class_dict: dict, code: tuple):
    """
    Places parallel classes with a given duration. Each key in class_dict
    represents a group (e.g., curriculum) that must be scheduled in the
    same time slot across multiple rooms.

    Parameters:
    - arr_2d (np.ndarray): The scheduling array (T x R)
    - T (int): Number of time slots (rows)
    - R (int): Number of rooms (columns)
    - class_dict (dict): {group_id: num_classes} to place per group
    - code (tuple): (session, duration)

    Returns:
    - np.ndarray: The updated arr_2d after placing the classes

    Raises:
    - RuntimeError if any group cannot be placed
    """
    if not class_dict:
        return arr_2d

    (session, duration) = code

    time_indices = [
        t for t in range(T - duration + 1)
        if (t % 10) <= (10 - duration)
    ]
    np.random.shuffle(time_indices)

    room_indices = [i for i in range(R)]

    used = get_used_slots(arr_2d)
    used_time_slot = {t for t, _ in used}

    for curr_id, n_classes in class_dict.items():
        placed = False

        subject_days = get_subject_days(arr_2d, curr_id)

        np.random.shuffle(room_indices)
        for t in time_indices:
            if t // 10 in subject_days:
                continue

            if t in used_time_slot or t + duration - 1 in used_time_slot:
                continue

            available_rooms = []
            for r in room_indices:
                if all((t + d, r) not in used for d in range(duration)):
                    available_rooms.append(r)
                if len(available_rooms) == n_classes:
                    break

            if len(available_rooms) == n_classes:
                class_no = 1
                for r in available_rooms:
                    for d in range(duration):
                        arr_2d[t + d, r] = 100 * curr_id + 10 * class_no + session
                        used.add((t + d, r))
                        used_time_slot.add(t + d)
                    class_no += 1

                time_indices = [ti for ti in time_indices if not (t <= ti <= t + duration)]
                placed = True
                break

        if not placed:
            raise RuntimeError(f"Cannot place group {curr_id} with {n_classes} classes (duration={duration})")

    return arr_2d

def get_used_slots(arr_2d):
    """
    Returns a set of (time, room) pairs that are already occupied in arr_2d.

    Parameters:
    - arr_2d (np.ndarray): 2D array of shape (T, R) representing schedule

    Returns:
    - Set of tuples (t, r) where arr_2d[t, r] is not 0
    """
    T, R = arr_2d.shape
    return {
        (t, r)
        for t in range(T)
        for r in range(R)
        if arr_2d[t, r] != 0
    }

def get_subject_days(arr_2d: np.ndarray, subject_id: int, slots_per_day: int = 10) -> set:
    """
    Determine on which days a given subject (group_id) appears in the schedule.

    Parameters:
    - arr_2d (np.ndarray): Schedule array of shape (T, R)
    - subject_id (int): The group ID to check (encoded in the hundreds digit of arr_2d values)
    - slots_per_day (int): Number of time slots per day (default is 10)

    Returns:
    - set: A set of integers representing the day indices on which the subject appears
    """
    subject_days = set()
    for t in range(arr_2d.shape[0]):
        for r in range(arr_2d.shape[1]):
            val = arr_2d[t, r]
            if val != 0 and val // 100 == subject_id:
                day = t // slots_per_day
                subject_days.add(day)
    return subject_days
