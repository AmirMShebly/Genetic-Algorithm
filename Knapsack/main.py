import random


def generate_population(pop_size):
    return [[random.choice([0, 1]) for _ in range(len(items))] for _ in range(pop_size)]


def fitness(individual):
    total_weight = sum(item["weight"] * bit for item, bit in zip(items, individual))
    total_value = sum(item["value"] * bit for item, bit in zip(items, individual))

    if total_weight > knapsack_capacity:
        return 0
    else:
        return total_value


def crossover(parent1, parent2, crossover_rate):
    if random.random() <= crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        child1, child2 = parent1, parent2
    return child1, child2


def mutate(individual, mutation_rate):
    return [bit if random.uniform(0, 1) > mutation_rate else 1 - bit for bit in individual]


def genetic_algorithm(pop_size, generations,elitism_ratio, mutation_rate, crossover_rate):
    population = generate_population(pop_size)

    for generation in range(generations):
        population = sorted(population, key=fitness, reverse=True)

        elite_size = int(elitism_ratio * pop_size)
        elites = population[:elite_size]
        selected_parents = population[:pop_size - elite_size]

        new_population = elites
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(selected_parents, 2)
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    return max(population, key=fitness)


items = [
    {"weight": 2, "value": 10},
    {"weight": 3, "value": 5},
    {"weight": 5, "value": 15},
    {"weight": 7, "value": 7},
    {"weight": 1, "value": 6}
]

knapsack_capacity = 10
population_size = 100
generations = 100
mutation_rate = 0.1
crossover_rate = 0.95
elitism_ratio = 0.1

result = genetic_algorithm(population_size, generations,elitism_ratio, mutation_rate, crossover_rate)
print("Optimal combination for the Knapsack Problem:", result)
