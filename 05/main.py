from collections import defaultdict
import random
import tqdm
import numpy as np
from itertools import permutations

rules = open('rules.txt', 'r').read()
rules = rules.split('\n')

rules = [x.split('|') for x in rules]
rules_dict = defaultdict(set)
for r in rules:
    rules_dict[int(r[0])].add(int(r[1]))

data = open('input.txt', 'r').read()
data = data.split('\n')

data = [list(map(int, x.split(','))) for x in data]

# First part

data_correct = []
data_incorrect = []
for d in data:
    seen = set()
    correct = True
    for x in d:
        seen.add(x)
        if x in rules_dict:
            rules_set = rules_dict[x]
            # Check if rules_set and seen are disjoint
            if not rules_set.isdisjoint(seen):
                correct = False
                data_incorrect.append(d)
                break

    if correct:
        data_correct.append(d)


# Extract middle parts of lists
res = 0
for d in data_correct:
    res += int(d[len(d)//2])
print(res)

# Second part


class SortableonRules:
    def __init__(self, x):
        self.x = x

    def __lt__(self, other):
        try:
            return other.x in rules_dict[self.x]
        except KeyError:
            return False

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)


data_corrected = []
for d in data_incorrect:
    d = [SortableonRules(x) for x in d]
    d.sort()
    data_corrected.append(d)


res = 0
for d in data_corrected:
    res += int(d[len(d)//2].x)
print(res)
