import random


def fitness(board):
    clashes = 0
    clashes += abs(len(board) - len(set(board)))

    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if abs(i - j) == abs(board[i] - board[j]):
                clashes += 1

    return 1 / (clashes + 1)


def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        child1, child2 = parent1, parent2

    return child1, child2


def mutate(child, mutation_rate):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(child) - 1)
        child[idx] = random.randint(0, len(child) - 1)
    return child


def genetic_algorithm(population_size, generations, mutation_rate, crossover_rate, board_size, elitism_ratio):
    population = [[random.randint(0, board_size - 1) for _ in range(board_size)] for _ in range(population_size)]

    for gen in range(generations):
        population = sorted(population, key=lambda x: fitness(x), reverse=True)

        if fitness(population[0]) == 1:
            return population[0]

        elite_size = int(elitism_ratio * population_size)
        elites = population[:elite_size]
        selected_parents = population[:population_size - elite_size]

        new_population = elites

        for _ in range(int(population_size / 2) - 1):
            parent1, parent2 = random.choices(selected_parents[:int(population_size / 2)], k=2)
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    return None


def draw_board(solution):
    n = len(solution)
    for i in range(n):
        for j in range(n):
            if solution[i] == j:
                print(" Q ", end="")
            else:
                print(" - ", end="")
        print()


population_size = 500
generations = 1000
mutation_rate = 0.2
crossover_rate = 0.95
board_size = 8
elitsm_ratio = 0.1

solution = genetic_algorithm(population_size, generations, mutation_rate, crossover_rate, board_size, elitsm_ratio)

if solution:
    print("Solution found: ", solution)
    draw_board(solution)
else:
    print("No solution found.")

