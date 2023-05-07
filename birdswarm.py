import numpy as np

class Particle:
    def __init__(self, n):
        self.position = np.random.randint(2, size=n)
        self.velocity = np.random.rand(n)
        self.best_position = self.position.copy()
        self.best_fitness = -1

def knapsack_fitness(position, weights, values, capacity):
    total_weight = np.sum(position * weights)
    total_value = np.sum(position * values)
    if total_weight > capacity:
        total_value -= (total_weight - capacity) * 10  # Penalty for exceeding capacity
    return total_value

def update_velocity(particle, global_best_position, w, c1, c2):
    r1, r2 = np.random.rand(2, particle.position.size)
    inertia = w * particle.velocity
    cognitive = c1 * r1 * (particle.best_position - particle.position)
    social = c2 * r2 * (global_best_position - particle.position)
    new_velocity = inertia + cognitive + social
    return new_velocity

def pso_knapsack(n, weights, values, capacity, num_particles=200, num_generations=500, w=0.5, c1=3, c2=1):
    swarm = [Particle(n) for _ in range(num_particles)]
    global_best_position = swarm[0].position
    global_best_fitness = knapsack_fitness(global_best_position, weights, values, capacity)

    for _ in range(num_generations):
        for particle in swarm:
            fitness = knapsack_fitness(particle.position, weights, values, capacity)

            if fitness > particle.best_fitness:
                particle.best_fitness = fitness
                particle.best_position = particle.position.copy()

                if fitness > global_best_fitness:
                    global_best_fitness = fitness
                    global_best_position = particle.position.copy()

            particle.velocity = update_velocity(particle, global_best_position, w, c1, c2)
            particle.position = (particle.position + particle.velocity > 0.5).astype(int)

    return global_best_position, global_best_fitness



import random

def generate_knapsack_dataset(n, weight_range=(1, 100), value_range=(1, 100)):
    weights = [random.randint(weight_range[0], weight_range[1]) for _ in range(n)]
    values = [random.randint(value_range[0], value_range[1]) for _ in range(n)]
    capacity = int(sum(weights) * 0.6)  # 60% of the total weight of items
    return weights, values, capacity

n = 20
weights, values, capacity = generate_knapsack_dataset(n)


def greedy_knapsack(n, weights, values, capacity):
    value_to_weight_ratios = [(i, v / w) for i, (v, w) in enumerate(zip(values, weights))]
    sorted_ratios = sorted(value_to_weight_ratios, key=lambda x: x[1], reverse=True)
    
    selected_items = []
    total_weight = 0
    total_value = 0
    
    for i, ratio in sorted_ratios:
        if total_weight + weights[i] <= capacity:
            total_weight += weights[i]
            total_value += values[i]
            selected_items.append(i)
    
    return selected_items, total_value


# Solve using the PSO-based solution
pso_solution, pso_fitness = pso_knapsack(n, weights, values, capacity)

# Solve using the greedy algorithm
greedy_solution, greedy_fitness = greedy_knapsack(n, weights, values, capacity)

print("PSO solution:", pso_solution, "Total value:", pso_fitness)
print("Greedy solution:", greedy_solution, "Total value:", greedy_fitness)
