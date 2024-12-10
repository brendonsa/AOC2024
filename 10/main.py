import numpy as np


data = open('input.txt', 'r').read()
data = data.split('\n')

data = [list(map(int,list(x))) for x in data]
data = np.array(data)

STEP_UP = (-1, 0)
STEP_RIGHT = (0, 1)
STEP_DOWN = (1, 0)
STEP_LEFT = (0, -1)

directions = [STEP_UP, STEP_RIGHT, STEP_DOWN, STEP_LEFT]

scores = np.zeros_like(data, dtype=int)

def is_legible(curr,step):
    next_a, next_b = curr[0] + step[0], curr[1]+ step[1]
    if next_a < 0 or next_b < 0:
        return False
    elif next_a >= data.shape[0] or next_b >= data.shape[0]:
        return False
    else:
        curr_value = data[curr[0],curr[1]]
        next_value = data[next_a,next_b]
        if curr_value+1!=next_value:
            return False
    return True

def walk(curr):
    curr_value = data[curr[0]][curr[1]]
    visited = set()
    if curr_value == 9:
        return {curr}
    else:
        for d in directions:
            if is_legible(curr,d):
                step = (curr[0]+d[0],curr[1]+d[1])
                visited = visited.union(walk(step))
    return visited


for i, d in enumerate(data):
    for j in range(len(d)):
        if d[j] == 0:
            scores[i,j] = len(walk((i,j)))
        
print(np.sum(scores))

# Second part. Instead of union lets just sum the paths
# If one would like to reuse the same function you would need to replace set with list
# Then for the first part turn it to a set and measure its len
# For the second part just use the len on the list.

def walk(curr):
    curr_value = data[curr[0]][curr[1]]
    visited = 0
    if curr_value == 9:
        return 1
    else:
        for d in directions:
            if is_legible(curr,d):
                step = (curr[0]+d[0],curr[1]+d[1])
                visited = visited+ walk(step)
    return visited


for i, d in enumerate(data):
    for j in range(len(d)):
        if d[j] == 0:
            scores[i,j] = walk((i,j))
        
print(np.sum(scores))