import numpy as np
from itertools import permutations

data = open('input.txt', 'r').read()
data = data.split('\n')

data = [list(d) for d in data]
data = np.array(data)

pos_antinodes = np.zeros_like(data, dtype=bool)


def test_in_bounds(data,point):
    if point[0]<0 or point[1] < 0:
        return False
    if point[0] >= data.shape[0] or point[1] >= data.shape[1]:
        return False
    return True


# First part
unique = np.unique(data)
pos = 0
for u in unique:
    if u == '.':
        continue
    common_freq = np.argwhere(data==u)
    for a,b in permutations(common_freq,2):
        diff = a-b
        antinode = a + diff
        if(test_in_bounds(data,antinode)):
            pos_antinodes[antinode[0],antinode[1]] = True
print(np.sum(pos_antinodes))

# Second part
pos_antinodes = np.zeros_like(data, dtype=bool)

unique = np.unique(data)
pos = 0
for u in unique:
    if u == '.':
        continue
    common_freq = np.argwhere(data==u)
    for a,b in permutations(common_freq,2):
        diff = a-b
        oob = False
        i = 0
        # Antennas fall in same line so they are antinodes
        pos_antinodes[a[0],a[1]] = True
        pos_antinodes[b[0],b[1]] = True
        while not oob:
            # Same as before, but now place them every i times distance
            i+=1
            antinode = a + i*diff
            if(test_in_bounds(data,antinode)):
                pos_antinodes[antinode[0],antinode[1]] = True
            else:
                oob = True
print(np.sum(pos_antinodes))
