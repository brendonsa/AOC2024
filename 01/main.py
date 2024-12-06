import numpy as np
# Read input from input.txt
data = open('input.txt', 'r').read()


# Split column data into two lists
data = data.split('\n')
array = np.ones((len(data), 2))
for idx, d in enumerate(data):
    d = d.split('   ')
    d = [int(x) for x in d]
    array[idx] = d
array = np.sort(array, axis=0)
array = array.astype(int)

# First part
diff = np.abs(np.diff(array, axis=1))
print(np.sum(diff))

# Second part
l, r = array[:, 0], array[:, 1]
unique_r, counts = np.unique(r, return_counts=True)

unique_dict = dict(zip(unique_r, counts))
intersection = (set(l).intersection(unique_r))
similarity = 0
for i in intersection:
    similarity += unique_dict[i]*i
print(similarity)
