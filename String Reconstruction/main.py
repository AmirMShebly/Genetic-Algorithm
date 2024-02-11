import random

gene_pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,!"


def generate_population(pop_size):
    return [''.join(random.choice(gene_pool) for _ in range(len(target_string))) for _ in range(pop_size)]


def fitness(individual):
    return sum(1 for a, b in zip(individual, target_string) if a == b)


def crossover(parent1, parent2, crossover_rate):
    if random.random() <= crossover_rate:
        crossover_point = random.randint(1, len(target_string) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        child1, child2 = parent1, parent2
    return child1, child2


def mutate(individual, mutation_rate):
    return ''.join(c if random.uniform(0, 1) > mutation_rate else random.choice(gene_pool) for c in individual)


def genetic_algorithm(target_string, population_size, generations, mutation_rate, crossover_rate, elitism_ratio):
    population = generate_population(population_size)

    for generation in range(generations):
        population = sorted(population, key=fitness, reverse=True)

        if fitness(population[0]) == len(target_string):
            return population[0]

        elite_size = int(elitism_ratio * population_size)
        elites = population[:elite_size]
        selected_parents = population[:population_size - elite_size]

        new_population = elites
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_parents, 2)
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    return max(population, key=fitness)


population_size = 100
generations = 1000
mutation_rate = 0.01
crossover_rate = 0.95
elitism_ratio = 0.1
target_string = "This Genetic Algorithm reconstructs any arbitrary string"

result = genetic_algorithm(target_string, population_size, generations, mutation_rate, crossover_rate, elitism_ratio)
print(result)
