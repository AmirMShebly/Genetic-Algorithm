import random
import math
import matplotlib.pyplot as plt


def read_cities(file_name):
    cities = []
    with open(file_name, 'r') as file:
        for line in file:
            data = line.split()
            city_num = int(data[0])
            x_coord = int(data[1])
            y_coord = int(data[2])
            cities.append((city_num, x_coord, y_coord))
    return cities


def euclidean_distance(cities):
    dist = 0
    for i in range(len(cities) - 1):
        city1 = cities[i]
        city2 = cities[i + 1]
        dist += math.sqrt((city2[1] - city1[1]) ** 2 + (city2[2] - city1[2]) ** 2)
    return dist


def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(0, len(cities) - 1)
        child1 = parent1[1][:crossover_point] + [gene for gene in parent2[1] if gene not in parent1[1][:crossover_point]]
        child2 = parent2[1][:crossover_point] + [gene for gene in parent1[1] if gene not in parent2[1][:crossover_point]]
    else:
        child1, child2 = parent1[1], parent2[1]

    return child1, child2


def mutate(child, mutation_rate):
    if random.random() <= mutation_rate:
        point1 = random.randint(0, len(cities) - 1)
        point2 = random.randint(0, len(cities) - 1)
        child[point1], child[point2] = child[point2], child[point1]
    return child


def genetic_algorithm(cities, population_size, generations, mutation_rate, crossover_rate, elitism_ratio):
    population = []

    for i in range(len(cities)):
        distance = euclidean_distance(cities)
        population.append([distance, cities])

    for _ in range(generations):
        new_population = []

        population.sort(key=lambda x: x[0])

        elites = population[:int(elitism_ratio * population_size)]

        new_population.extend(elites)

        while len(new_population) < population_size:
            parent1 = sorted(random.choices(population, k=4))[0]
            parent2 = sorted(random.choices(population, k=4))[0]

            child1, child2 = crossover(parent1, parent2, crossover_rate)

            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.extend([[euclidean_distance(child1), child1], [euclidean_distance(child2), child2]])

        population = new_population

    best_route = sorted(population)[0]

    return best_route


population_size = 400
generations = 1000
mutation_rate = 0.3
crossover_rate = 0.95
elitism_ratio = 0.1

cities = read_cities("TSP51.txt")

best_route = genetic_algorithm(cities, population_size, generations, mutation_rate, crossover_rate, elitism_ratio)

sequence_of_cities = best_route[1]
city_numbers = [city[0] for city in sequence_of_cities]
print("Sequence of cities:", city_numbers)
print("Total traversed distance: ", best_route[0])

for city in cities:
    plt.plot(city[1], city[2])
    plt.annotate(city[0], (city[1], city[2]))

for i in range(len(best_route[1]) - 1):
    source = best_route[1][i]
    dest = best_route[1][i + 1]

    plt.plot([source[1], dest[1]], [source[2], dest[2]], color="blue")

plt.title('Best route found by the GA')
plt.show()



