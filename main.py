from utils import io

from dataframes.curriculum import Curriculum
from dataframes.subject import Subject
from dataframes.time_slot import TimeSlot
from dataframes.room import Room

from ga.genome import Genome
from ga.genetic_algorithm import GeneticAlgorithm, ProblemContext

if __name__ == '__main__':
    subjects = Subject("csv/subjects.csv")
    curriculum = Curriculum("csv/curriculum.csv", subjects.df)

    # time_slots = TimeSlot("csv/time_slots.csv").df
    # time_slot_indices = time_slots['id'].to_list()

    # rooms = Room('csv/rooms.csv').df
    # big_rooms = rooms[rooms['capacity'] >= 100]
    # room_indices = big_rooms['id'].to_list()

    context = ProblemContext(
        curriculum=curriculum,
        time_slot_indices=list(range(40)),
        room_indices=list(range(24))
    )

    ga = GeneticAlgorithm(context=context, population_size=10)
    # ga.run()

