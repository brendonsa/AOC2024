from matplotlib import pyplot as plt
import numpy as np
data = open('input.txt', 'r').read()
data = data.split('\n')

data = [list(d) for d in data]
visited = np.zeros((len(data), len(data[0])), dtype=bool)

STEP_UP = (-1, 0)
STEP_RIGHT = (0, 1)
STEP_DOWN = (1, 0)
STEP_LEFT = (0, -1)

directions = [STEP_UP, STEP_RIGHT, STEP_DOWN, STEP_LEFT]


def out_of_bounds(next_a, next_b):
    if next_a < 0 or next_b < 0:
        return True
    elif next_a >= len(data) or next_b >= len(data[0]):
        return True


def is_legible(idx, step, visited):
    next_a, next_b = idx[0]+step[0], idx[1]+step[1]
    if out_of_bounds(next_a, next_b):
        return False
    elif visited[next_a, next_b]:
        return False
    return True


def walk(idx):
    global visited
    visited[idx[0], idx[1]] = True
    perimeter = 4
    plot = 1
    # Addition for part two
    value = data[idx[0]][idx[1]]
    for d in directions:
        if is_legible(idx, d, visited):
            value_neighbour = data[idx[0]+d[0]][idx[1]+d[1]]
            if value_neighbour == value:
                perimeter -= 1
                perimeter_neigh, plot_neigh = walk([idx[0]+d[0], idx[1]+d[1]])
                perimeter += perimeter_neigh
                plot += plot_neigh
# Not effective, should only check once but IDC
        elif not out_of_bounds(idx[0]+d[0], idx[1]+d[1]):
            value_neighbour = data[idx[0]+d[0]][idx[1]+d[1]]
            if value_neighbour == value:
                perimeter -= 1
    return perimeter, plot


def trim_and_pad(nparray):
    # Trim values so the sides only contain True
    rows, cols = np.where(nparray)
    row_start, row_end = rows.min(), rows.max() + 1
    col_start, col_end = cols.min(), cols.max() + 1
    trimmed_array = nparray[row_start:row_end, col_start:col_end]

    padded_array = np.pad(trimmed_array, pad_width=1,
                          mode='constant', constant_values=False)
    return padded_array


def count_edges_LR(visited):
    edge_positions = np.zeros_like(visited, dtype=bool)
    edge_positions = np.diff(visited, axis=1)
    edge_positions[edge_positions < 0] = 0
    transitions = np.diff(edge_positions, axis=0)
    start_indices = np.where(transitions == 1)[0]
    return len(start_indices)


score_first = 0
score_second = 0
for i in range(len(data)):
    for j in range(len(data[0])):
        if not visited[i, j]:
            visited_temp = visited.copy()
            perimeter, plot = walk([i, j])
            score_first += perimeter*plot
            visited_this = np.logical_xor(visited_temp, visited)
            visited_this = trim_and_pad(visited_this)
            visited_this = visited_this.astype(int)
            count_right = count_edges_LR(visited_this)
            count_up = count_edges_LR(visited_this.T)
            count_left = count_edges_LR(visited_this[:, ::-1])
            count_down = count_edges_LR(visited_this[::-1].T)
            sides = count_right+count_up+count_left+count_down
            score_second += sides*plot


print(score_first)
print(score_second)
