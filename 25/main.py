import numpy as np

data = open('input.txt').read().replace('#','1').replace('.','0').split('\n')

keys = []
locks = []
for idx in range(1+len(data)//8):
    i = idx*8
    if data[i][0] == '1':
        val = data[i+1:i+6]
        val = [list(map(int,v)) for v in val]
        locks.append(np.array(val)*-1)
    elif data[i][0] == '0':
        val = data[i+1:i+6]
        val = [list(map(int,v)) for v in val]
        keys.append(np.array(val))
    else:
        continue

keys = np.array(keys)
locks = np.array(locks)
good_combinations = 0
differences = locks[:, np.newaxis, :, :] - keys[np.newaxis, :, :, :]  # Shape (249, 250, 5, 5)
min_differences = np.min(differences, axis=(-2, -1))  # Shape (249, 250)
print(np.sum(min_differences>-2))
