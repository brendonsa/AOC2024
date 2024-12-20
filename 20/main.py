import numpy as np
import heapq
from matplotlib import pyplot as plt


data = open('input.txt').read()
data = [list(d) for d in data.split('\n')]
data = np.array(data)


EAST = (0, 1)
WEST = (0, -1)
NORTH = (-1, 0)
SOUTH = (1, 0)

directions = [EAST, WEST, NORTH, SOUTH]
distances = np.ones_like(data, dtype=int) * -1


def out_of_bounds(next_a, next_b):
    if next_a < 0 or next_b < 0:
        return True
    elif next_a >= data.shape[0] or next_b >= data.shape[1]:
        return True


start_point = np.where(data == 'S')
start_point = (start_point[0][0], start_point[1][0])
end_point = np.where(data == 'E')
end_point = (end_point[0][0], end_point[1][0])
distances[start_point] = 0
QUEUE = []
heapq.heappush(QUEUE, (0, start_point))

while QUEUE:
    dist_here, position = heapq.heappop(QUEUE)
    if position == end_point:
        break
    for d in directions:
        new_position = (position[0]+d[0], position[1]+d[1])
        if data[new_position] == '#':
            continue
        if not out_of_bounds(new_position[0], new_position[1]):
            if distances[new_position[0], new_position[1]] > dist_here+1 or distances[new_position[0], new_position[1]] == -1:
                distances[new_position[0], new_position[1]] = dist_here+1
                heapq.heappush(
                    QUEUE, (dist_here+1, new_position))


end_position_dist = distances[end_point]
a = 0
for i in range(end_position_dist-100):
    position_curr = np.where(distances == i)
    position_curr = (position_curr[0][0], position_curr[1][0])
    for d in directions:
        new_position = (position_curr[0]+d[0]*2, position_curr[1]+d[1]*2)
        if not out_of_bounds(new_position[0], new_position[1]):
            distance_new = distances[new_position[0], new_position[1]]
            if distance_new - i - 1 > 100:
                # -1 is needed to offset the cheat that you took
                a += 1

print(a)


def build_cityblock_offsets(max_distance):
    offsets = []
    for dx in range(-max_distance, max_distance + 1):
        for dy in range(-max_distance, max_distance + 1):
            if abs(dx) + abs(dy) <= max_distance:
                offsets.append((dx, dy))
    return np.array(offsets)


def apply_offsets_to_center(grid_shape, center, offsets):
    rows, cols = grid_shape
    x0, y0 = center

    shifted_indices = offsets + np.array([x0, y0])

    valid_indices = shifted_indices[
        (shifted_indices[:, 0] >= 0) & (shifted_indices[:, 0] < rows) &
        (shifted_indices[:, 1] >= 0) & (shifted_indices[:, 1] < cols)
    ]

    return valid_indices


def calc_cityblock(pointA, pointB):
    return np.sum(np.abs(pointA - pointB), axis=1)


cityblock = build_cityblock_offsets(20)
# distances[np.where(distances == -1)] = -1
a = 0
for i in range(end_position_dist-100):
    position_curr = np.where(distances == i)
    position_curr = (position_curr[0][0], position_curr[1][0])
    points = apply_offsets_to_center(data.shape, position_curr, cityblock)
    distances_cityblock = distances[points[:, 0], points[:, 1]]
    distances_to_check = calc_cityblock(position_curr, points)
    a += np.sum((distances_cityblock - distances_to_check - i+1) > 100)

print(a)
