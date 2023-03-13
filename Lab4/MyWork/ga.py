import random

p_mutation = 0.8
num_of_generations = 30


# noinspection DuplicatedCode
def genetic_algorithm(population: set[tuple], fitness_fn, minimal_fitness: float) -> tuple:
    generation = ()
    fittest_individual = ()
    for generation in range(num_of_generations):
        print(f"Generation {generation}:")
        print_population(population, fitness_fn)

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

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print(f"Final generation {generation}:")
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population: set[tuple], fitness_fn) -> None:
    for individual in population:
        fitness = fitness_fn(individual)
        print(f"{individual} - fitness: {fitness}")


def reproduce(mother: tuple, father: tuple) -> tuple:
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''

    crossover_index = 1

    # child = (*mother[:crossover_index], *father[crossover_index:])
    child = mother[:crossover_index] + father[crossover_index:]
    print(child)
    return child


def mutate(individual: tuple) -> tuple:
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''

    index = random.randint(0, len(individual) -1)

    mutation = individual[:index] + tuple([random.randint(0, 1)]) + individual[index + 1:]
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

    return mother, father


def fitness_function(individual: tuple) -> float:
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''

    fitness = 0
    k = len(individual) - 1
    for v in individual:
        fitness += v * (2 ** k)
        k -= 1

    return fitness


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
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    # initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
