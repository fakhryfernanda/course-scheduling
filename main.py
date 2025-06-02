from utils import io

from dataframes.curriculum import Curriculum
from dataframes.subject import Subject
from dataframes.course import Course
from dataframes.time_slot import TimeSlot
from dataframes.room import Room

from ga.genome import Genome

if __name__ == '__main__':
    subjects = Subject("csv/subjects.csv")
    courses = Course("csv/fmipa.csv")
    curriculum = Curriculum("csv/curriculum.csv", subjects.df, courses.df)

    time_slots = TimeSlot("csv/time_slots.csv").df
    time_slot_indices = time_slots['id'].to_list()

    rooms = Room('csv/rooms.csv').df
    big_rooms = rooms[rooms['capacity'] >= 100]
    room_indices = big_rooms['id'].to_list()

    genome = Genome.from_generator(curriculum, courses, time_slot_indices=range(20), room_indices=range(12))
    
    for i in range(10):
        io.export_to_txt(genome.chromosome, "solutions", f"solution_{i+1}.txt")