import random


def generate_population(pop_size, list_size):
    population = []
    for _ in range(pop_size):
        individual = list(range(1, list_size + 1))
        random.shuffle(individual)
        population.append(individual)
    return population


def fitness(individual):
    errors = 0
    length = len(individual)

    for i in range(length - 1):
        for j in range(i + 1, length):
            if individual[i] > individual[j]:
                errors += 1

    return 1 / (1 + errors)


def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2


def mutate(individual, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual


def genetic_algorithm(pop_size, list_size, generations, mutation_rate, elitism_ratio):
    population = generate_population(pop_size, list_size)

    for generation in range(generations):
        population = sorted(population, key=fitness, reverse=True)

        if fitness(population[0]) == 1:
            return population[0]

        elite_size = int(elitism_ratio * pop_size)
        elites = population[:elite_size]

        selected_parents = population[:pop_size - elite_size]

        new_population = elites
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(selected_parents, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    return max(population, key=calculate_fitness)


population_size = 100
list_size = 10
generations = 100
mutation_rate = 0.1
elitism_ratio = 0.1

result = genetic_algorithm(population_size, list_size, generations, mutation_rate, elitism_ratio)
print("Sorted List found by the GA:", result)

