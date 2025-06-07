from typing import Final

LOG_EVALUATION: Final[bool] = True
SLOTS_PER_DAY: Final[int] = 10

POPULATION_SIZE: Final[int] = 10
MAX_GENERATION: Final[int] = 200
CROSSOVER_RATE: Final[float] = 0.7
MUTATION_RATE: Final[float] = 0.1

SELECTION_METHOD: Final[str] = "tournament"
RANDOMIZE_CROSSOVER: Final[bool] = True
MUTATION_METHOD: Final[str] = "random_swap"