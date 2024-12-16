from matplotlib import pyplot as plt
import numpy as np

data = open('input.txt', 'r').read()
data = data.split('\n')
data = [list(d) for d in data]

EAST = (0, 1)
WEST = (0, -1)
NORTH = (-1, 0)
SOUTH = (1, 0)

reverse = {EAST: WEST,
           WEST: EAST,
           NORTH: SOUTH,
           SOUTH: NORTH}


data = np.array(data)

starting_position = np.where(data == 'S')
end_position = np.where(data == 'E')
end_position = (end_position[0][0], end_position[1][0])
starting_position = (starting_position[0][0], starting_position[1][0])
distances = np.ones_like(data, dtype=int) * 10000000000000000
distances[starting_position] = 0
came_from = np.array([[[None, None, None] for _ in range(data.shape[0])]
                     for _ in range(data.shape[1])])


def lookaround(position, direction, new_dirs, QUEUE, DISTANCES):
    new_position = (position[0] + direction[0], position[1]+direction[1])
    if data[new_position] not in ['#', 'S']:
        new_direction = direction
        if distances[new_position] > distances[position] + 1:
            distances[new_position] = distances[position] + 1
            QUEUE.append((new_position, new_direction))
            DISTANCES.append(distances[new_position])
            came_from[new_position[0]][new_position[1]] = [
                position[0], position[1], reverse[direction]]

    for direction in new_dirs:
        new_position = (position[0] + direction[0], position[1]+direction[1])
        if data[new_position] not in ['#', 'S']:
            new_direction = direction
            if distances[new_position] > distances[position] + 1001:
                distances[new_position] = distances[position] + 1001
                came_from[new_position[0]][new_position[1]] = [
                    position[0], position[1], reverse[direction]]
                QUEUE.append((new_position, new_direction))
                DISTANCES.append(distances[new_position])
    return QUEUE, DISTANCES


QUEUE = [(starting_position, EAST)]
DISTANCES = [0]

while len(QUEUE) > 0:
    distances_min = np.argsort(DISTANCES)[0]
    DISTANCES.pop(distances_min)
    position, direction = QUEUE.pop(distances_min)
    if direction == EAST:
        QUEUE, DISTANCES = lookaround(
            position, direction, [NORTH, SOUTH], QUEUE, DISTANCES)
    elif direction == WEST:
        QUEUE, DISTANCES = lookaround(
            position, direction, [NORTH, SOUTH], QUEUE, DISTANCES)
    elif direction == NORTH:
        QUEUE, DISTANCES = lookaround(
            position, direction, [EAST, WEST], QUEUE, DISTANCES)
    elif direction == SOUTH:
        QUEUE, DISTANCES = lookaround(
            position, direction, [EAST, WEST], QUEUE, DISTANCES)

distances[distances == 10000000000000000] = -1
np.savetxt("out.csv", distances, delimiter=",", fmt="%d")

plt.imshow(distances)
plt.show()
