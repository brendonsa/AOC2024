from matplotlib import pyplot as plt
import numpy as np

data = open('input.txt', 'r').read()
data = data.split('\n')
data = [list(map(int, d.split(','))) for d in data]

EAST = (0, 1)
WEST = (0, -1)
NORTH = (-1, 0)
SOUTH = (1, 0)

directions = [EAST, WEST, NORTH, SOUTH]

mem_map = np.ones((71, 71))

for idx, d in enumerate(data):
    if idx == 1024:
        break
    mem_map[d[1], d[0]] = 0

distances = np.ones_like(mem_map) * -1
start_point = (0, 0)
distances[0, 0] = 0


QUEUE = [start_point]
DISTANCES = [0]


def out_of_bounds(next_a, next_b):
    if next_a < 0 or next_b < 0:
        return True
    elif next_a >= mem_map.shape[0] or next_b >= mem_map.shape[1]:
        return True


while len(QUEUE) > 0:
    distances_min = np.argsort(DISTANCES)[0]
    dist_here = DISTANCES.pop(distances_min)
    position = QUEUE.pop(distances_min)
    for d in directions:
        new_position = (position[0]+d[0], position[1]+d[1])

        if not out_of_bounds(new_position[0], new_position[1]):
            if mem_map[new_position[0], new_position[1]] == 0:
                continue
            if distances[new_position[0], new_position[1]] > dist_here+1 or distances[new_position[0], new_position[1]] == -1:
                distances[new_position[0], new_position[1]] = dist_here+1
                DISTANCES.append(dist_here+1)
                QUEUE.append(new_position)

print(distances[70, 70])


def simulate_bytes(quantity):
    mem_map = np.ones((71, 71))
    for idx, d in enumerate(data):
        if idx == quantity:
            break
        mem_map[d[1], d[0]] = 0
    QUEUE = [start_point]
    distances = np.ones_like(mem_map) * -1
    distances[0, 0] = 0
    DISTANCES = [0]
    while len(QUEUE) > 0:
        distances_min = np.argsort(DISTANCES)[0]
        dist_here = DISTANCES.pop(distances_min)
        position = QUEUE.pop(distances_min)
        for d in directions:
            new_position = (position[0]+d[0], position[1]+d[1])

            if not out_of_bounds(new_position[0], new_position[1]):
                if mem_map[new_position[0], new_position[1]] == 0:
                    continue
                if distances[new_position[0], new_position[1]] > dist_here+1 or distances[new_position[0], new_position[1]] == -1:
                    distances[new_position[0], new_position[1]] = dist_here+1
                    DISTANCES.append(dist_here+1)
                    QUEUE.append(new_position)
    return distances


for i in range(1024, len(data)):
    d = simulate_bytes(i)
    if d[70, 70] == -1:
        break


print(data[i-1])
