from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor
import numpy as np

data = open('input.txt', 'r').read()
data = data.split('\n')
data = [list(x) for x in data]


STEP_UP = (-1, 0)
STEP_RIGHT = (0, 1)
STEP_DOWN = (1, 0)
STEP_LEFT = (0, -1)


class DirectionWalk():
    def __init__(self):
        self.step = STEP_UP

    def rotate(self):
        if self.step == STEP_UP:
            self.step = STEP_RIGHT
        elif self.step == STEP_RIGHT:
            self.step = STEP_DOWN
        elif self.step == STEP_DOWN:
            self.step = STEP_LEFT
        elif self.step == STEP_LEFT:
            self.step = STEP_UP

    def __str__(self):
        return str(self.step)


def walk(data_p, initial_position=None):
    direction = DirectionWalk()
    if not initial_position:
        initial_position = (0, 0)
        for idx, d in enumerate(data_p):
            if '^' in d:
                initial_position = (idx, d.index('^'))
                break

    visited = set()
    visited.add((STEP_UP, initial_position))
    data_p[initial_position[0]][initial_position[1]] = 'V'
    curr_pos = initial_position
    data_p = deepcopy(data_p)
    while True:
        new_position = (curr_pos[0]+direction.step[0],
                        curr_pos[1]+direction.step[1])
        if (direction.step, new_position) in visited:
            raise ValueError('LOOP')
        try:
            if -1 in new_position:
                raise IndexError
            if data_p[new_position[0]][new_position[1]] == '#':
                direction.rotate()
            else:
                visited.add((direction.step, new_position))
                data_p[new_position[0]][new_position[1]] = 'V'
                curr_pos = new_position
        except IndexError:
            break
    return initial_position, data_p


initial_position, data_new = walk(data)
sum_v = 0
for row in data_new:
    sum_v += row.count('V')


print(sum_v)

# Second part


all_V_positions = []
for idx, row in enumerate(data_new):
    all_V_positions.extend([(idx, i) for i, x in enumerate(row) if x == 'V'])
all_V_positions.remove(initial_position)


def try_loop(pos):
    data_new = deepcopy(data)
    data_new[pos[0]][pos[1]] = '#'
    try:
        walk(data_new, initial_position)
    except ValueError:
        return True
    return False


with ProcessPoolExecutor() as executor:
    results = list(executor.map(try_loop, all_V_positions))

print(sum(results))
