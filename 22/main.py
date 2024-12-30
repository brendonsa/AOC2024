import numpy as np
data = open('input.txt').read()
data = list(map(int, data.split('\n')))

def mix(a,b):
    return a^b

def prune(a):
    return a % 16777216

a = 0
changes_all = []
values_all = []
for d in data:
    values = [d%10]
    for _ in range(2000):
        b = d*64
        d = mix(d,b)
        d = prune(d)
        b = d//32
        d = mix(d,b)
        d = prune(d)
        b = d*2048
        d = mix(d,b)
        d = prune(d)
        values.append(d%10)
    values_all.append(values)
    changes_all.append(np.diff(values))
    a +=d

print(a)

# Let's add all the sequences to numpy array? A little bit sparce. 4 dimensional.
# If the sequence was already seen for the buyer we add only the first one

results = np.zeros((20,20,20,20), dtype=int)

for values,changes in zip(values_all,changes_all):
    changes = np.array(changes)
    analyzed_sequences = set()
    for i in range(len(changes)-4):
        chunk = tuple(changes[i:i+4])
        if chunk in analyzed_sequences:
            continue
        analyzed_sequences.add(chunk)
        results[chunk] += values[i+4]


print(np.max(results))


