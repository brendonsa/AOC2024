import numpy as np
# Read input from input.txt
data = open('input.txt', 'r').read()

data = data.split('\n')
# Split every line on space
data = [x.split(' ') for x in data]
# Cast every list of lists to int
data = [[int(x) for x in y] for y in data]


def test_safe(data):
    diff = np.diff(data)
    if not all(diff < 0) and not all(diff > 0):
        return 0
    diff = np.abs(diff)
    if all(diff < 4):
        return 1
    return 0


# Part 1
safe = 0
for d in data:
    safe += test_safe(d)

print(safe)


# Part 2


def dampener_bruteforce(data):
    for idx in range(len(data)):
        data_n = np.delete(data, idx)
        safe = test_safe(data_n)
        if safe:
            return safe
    return 0


safe = 0
for d in data:
    safe_this = test_safe(d)
    if safe_this:
        safe += 1
        continue
    else:
        safe_brute = dampener_bruteforce(d)
        safe += safe_brute
        continue

print(safe)
