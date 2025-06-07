from globals import *
from dataframes.curriculum import Curriculum
from dataframes.subject import Subject
from ga.genetic_algorithm import GeneticAlgorithm, ProblemContext

if __name__ == '__main__':
    subjects = Subject("csv/subjects.csv")
    curriculum = Curriculum("csv/curriculum.csv", subjects.df)

    context = ProblemContext(
        curriculum=curriculum,
        time_slot_indices=list(range(30)),
        room_indices=list(range(24))
    )

    ga = GeneticAlgorithm(
        context=context, 
        population_size=POPULATION_SIZE, 
        max_generation=MAX_GENERATION,
        crossover_rate=CROSSOVER_RATE,
        mutation_rate=MUTATION_RATE
    )
