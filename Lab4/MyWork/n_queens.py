import random
import time

from Lab4.queens_fitness import fitness_fn_negative

p_mutation = 0.5
p_value_mutation = 0.5
num_of_generations = 100
population_size = 100


# noinspection DuplicatedCode
def genetic_algorithm(population: set[tuple], fitness_fn, minimal_fitness: float) -> tuple[tuple, set[tuple]]:
    generation = ()
    fittest_individual = ()
    for generation in range(num_of_generations):
        # print(f"Generation {generation}:")

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)
        population = trim_population(population, population_size, fitness_fn_negative)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print(f"Final generation {generation}:")
    print_population(population, fitness_fn)

    return fittest_individual, population


def trim_population(population: set[tuple], desired_length: int, fitness_fn) -> set[tuple]:
    trim_amount = len(population) - desired_length
    if trim_amount <= 0:
        return population

    # Will store tuples like (citizen: tuple, fitness: float)
    population_list = sorted(list(population), key=lambda x: fitness_fn(x), reverse=False)
    population_list = population_list[trim_amount:]

    return set(population_list)

    # lowest_fitness = sorted(population_list[:trim_amount], key=lambda x: fitness_fn(x), reverse=False)
    # lowest_fitness = [(x, fitness_fn(x)) for x in lowest_fitness]
    # for citizen in population_list[trim_amount:]:
    #     fitness = fitness_fn(citizen)
    #     for other in lowest_fitness:
    #         if


def print_population(population: set[tuple], fitness_fn) -> None:
    for individual in population:
        fitness = fitness_fn(individual)
        print(f"{individual} - fitness: {fitness}")


def reproduce(mother: tuple, father: tuple) -> tuple:
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''

    crossover_index = random.randint(1, len(mother) - 1)

    child = (*mother[:crossover_index], *father[crossover_index:])
    # child = mother[:crossover_index] + father[crossover_index:]
    # print(child)
    return child


def mutate(individual: tuple) -> tuple:
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    mutation = individual
    # index = random.randint(0, len(individual) - 1)
    for i, val in enumerate(individual):
        if random.random() <= p_value_mutation:
            mutation = (*individual[:i], random.randint(1, 8), *individual[i + 1:])

    # mutation = individual[:index] + tuple([random.randint(1, 8)]) + individual[index + 1:]
    return mutation


def random_selection(population: set[tuple], fitness_fn) -> tuple[tuple, tuple]:
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.

    ordered_population = list(population)

    fit_sum = 0

    for individual in ordered_population:
        fit_sum += fitness_fn(individual)

    father_choice = random.randint(1, 100)
    mother_choice = random.randint(1, 100)

    father = ()
    mother = ()

    running_sum = 0

    for individual in ordered_population:
        running_sum += fitness_fn(individual)
        if (running_sum / fit_sum) * 100 > mother_choice:
            mother = individual

    running_sum = 0

    for individual in ordered_population:
        running_sum += fitness_fn(individual)
        if (running_sum / fit_sum) * 100 > father_choice:
            father = individual

    if mother == ():
        mother = ordered_population[0]

    if father == ():
        father = ordered_population[len(ordered_population) - 1]

    return mother, father


def get_fittest_individual(iterable: set[tuple], func) -> tuple:
    return max(iterable, key=func)


def get_initial_population(n: int, count: int) -> set[tuple]:
    '''
    Randomly generate count individuals of length n
    Note since it's a set it disregards duplicate elements.
    '''

    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 0

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 2, 3, 4, 5, 6, 7, 8),
        (1, 1, 1, 1, 1, 1, 1, 1),
        (2, 2, 2, 2, 2, 2, 2, 2),
        (3, 3, 3, 3, 3, 3, 3, 3),
        (3, 2, 7, 1, 3, 8, 2, 5),
        (2, 2, 7, 1, 3, 8, 8, 5),
        (2, 2, 7, 1, 3, 8, 8, 5),
        (2, 4, 7, 1, 3, 6, 8, 5),
        (2, 4, 7, 1, 3, 8, 6, 8)
    }
    # initial_population = get_initial_population(3, 4)

    start_time = time.perf_counter_ns()
    fittest, final_generation = genetic_algorithm(initial_population, fitness_fn_negative, minimal_fitness)
    end_time = time.perf_counter_ns()
    print_population(final_generation, fitness_fn_negative)
    print(f"Fittest Individual: {fittest} - fitness: {fitness_fn_negative(fittest)}")
    print(f"total elapsed time: {(end_time - start_time) / 10**6} ms")


if __name__ == '__main__':
    main()
