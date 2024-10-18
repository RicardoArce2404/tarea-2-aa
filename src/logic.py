from random import choice, randint
from .socketio_setup import socketio
import eventlet

# Every individual is a list of booleans representing which items of the
# number set it includes. This facilitates mutation and breeding.

Individual = list[bool]

def get_fitness(number_set: list[int], individual: Individual, limit: int) -> int:
    """
    Returns the fitness value of an individual based on the values of its
    chromosomes in the given number set and the limit requested by the user.
    """

    fitness: int = 0
    for index, chromosome in enumerate(individual):  # Isn't AI. We know what it does.
        if chromosome == True:
            fitness += number_set[index]
    if fitness > limit:
        return 0  # Easy penalization technique but not ideal. May be changed.
    return fitness

def mutate(individual: Individual) -> None:
    """
    Mutates and individual by interchanging the truth value of its
    chromosomes between True and False with a 25% probability.
    """

    probability: int = 10
    for i in range(len(individual)):
        # Only 10% of that random integers will fall in the
        # [1, 10] range and therefore make the comparison True.
        if randint(1, 100) <= probability:
            individual[i] = not individual[i]  # Interchanges between True and False

def get_new_generation(parent1: Individual, parent2: Individual, amount: int) -> list[Individual]:
    """
    Returns a new generation of childs with a
    combination of the chromosomes of its parents.
    """

    length: int = len(parent1)
    new_generation: list[Individual] = []
    for _ in range(amount):
        child: Individual = [choice([parent1[i], parent2[i]]) for i in range(length)]
        mutate(child)
        new_generation.append(child)
    return new_generation

def get_solution(number_set: list[int], limit: int) -> list[int]:
    """
    Returns a list of integers that is the best choice of the elements of the
    given number set that maximizes its total value without exceding the given limit
    """

    POPULATION_SIZE: int = 5 # i put it to 5 for it to converge slower
    GENERATIONS: int = 100
    population: list[Individual] = []

    for _ in range(POPULATION_SIZE):
        population.append([choice([True, False]) for _ in range(len(number_set))])
    population.sort(key=lambda x: get_fitness(number_set, x, limit), reverse=True)

    best_individual: Individual = []
    for current_generation in range(GENERATIONS):
        population = get_new_generation(population[0], population[1], POPULATION_SIZE)
        population.sort(key=lambda x: get_fitness(number_set, x, limit), reverse=True)
        best_individual = population[0]
        best_fitness: int = get_fitness(number_set, best_individual, limit)
        
        # send updates to client
        state_data = create_json_update(number_set ,current_generation, best_individual, best_fitness)
        socketio.emit('update-state', state_data)
        eventlet.sleep(0.07)
        
        if best_fitness == limit:
            break

    solution: list[int] = []
    for i in range(len(number_set)):
        if best_individual[i] == True:
            solution.append(number_set[i])
    return solution

def get_individual_representation(number_set: list[int], individual) -> list[int]:
    """
    Returns a list of integers that is the best choice of the elements of the
    given number set that maximizes its total value without exceding the given limit
    """

    solution: list[int] = []
    for i in range(len(number_set)):
        if individual[i] == True:
            solution.append(number_set[i])
    return solution

def create_json_update(set: list[int], generation: int, individual: Individual, sum: int) -> dict:
    """
    Returns a dictionary with the information of the current generation
    for the emit event of the socketio server.
    """

    return {
        'set': set,
        'generation': generation,
        'solution': get_individual_representation(set, individual),
        'sum': sum
    }

# number_set = [randint(1, 20) for _ in range(10)]
# print(number_set)
# print(get_solution(number_set, 30))