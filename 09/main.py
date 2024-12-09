import numpy as np
from tqdm import tqdm
data = open('input.txt', 'r').read()
data = list(map(int, list(data)))

memory = np.zeros(sum(data), dtype=int)

curr_idx = 0
curr_id = 0
in_memory = True
for d in data:
    if in_memory:
        memory[curr_idx:curr_idx+d] = curr_id
        curr_id += 1
        in_memory = False
    else:
        memory[curr_idx:curr_idx+d] = -1
        in_memory = True
    curr_idx += d

index_of_negative = np.where(memory == -1)[0]
a = index_of_negative[0]
idx_negative = 0
b = len(memory)-1
while a < b:
    right_element = memory[b]
    if right_element == -1:
        b -= 1
        continue
    else:
        memory[a] = right_element
        memory[b] = -1
        idx_negative += 1
        a = index_of_negative[idx_negative]
        b -= 1

mem = memory[memory > -1]
mult = np.arange(len(mem))
print(sum(mult*mem))

memory_new = np.ones(((len(set(memory))-1)*2-1, 9), dtype=int) * -2

curr_id = 0
in_memory = True
free_space = np.zeros(len(memory_new), dtype=int)
for idx, d in enumerate(data):
    if in_memory:
        memory_new[idx, 0:d] = curr_id
        curr_id += 1
        in_memory = False
    else:
        memory_new[idx, 0:d] = -1
        free_space[idx] = d
        in_memory = True

# Free space solution
for i in tqdm(range(len(memory_new)-1, -1, -1)):
    if (all(memory_new[i] < 0)):
        # Nothing to transfer
        continue
    if (len(set(memory_new[i][memory_new[i] > 1])) > 1):
        # Already transfered
        continue
    length_needed = sum(memory_new[i] > -1)
    if length_needed == 0:
        continue
    free_indices = np.argwhere(free_space >= length_needed)
    if free_indices.size == 0:
        continue
    else:
        free_indices = free_indices[0]
    # print(free_indices)
    if free_indices.size > 0:
        # input()
        j = free_indices[0]
        if j > i:
            #  It means that it would be transfered to the right side.
            continue
        j_idx = np.argwhere(memory_new[j] == -1)[0][0]
        # print('Iš:', memory_new[i], 'Į:', memory_new[j],
        #   'Laisvos vietos indeksas:', j_idx, 'Laisvos vietos:', free_space[j])
        memory_new[j, j_idx:j_idx +
                   length_needed] = memory_new[i, :length_needed]
        memory_new[i, :length_needed] = -1
        free_space[j] = sum(memory_new[j] == -1)
        # print('Perkelta į :', memory_new[j], 'laisva vieta: ', free_space[j])


mem = memory_new[memory_new > -2]
mem_mult = np.arange(len(mem))
mem[mem == -1] = 0
print(sum(mem*mem_mult))

# Loop solution


memory_new = np.ones(((len(set(memory))-1)*2-1, 9), dtype=int) * -2

curr_id = 0
in_memory = True
free_space = np.zeros(len(memory_new), dtype=int)
for idx, d in enumerate(data):
    if in_memory:
        memory_new[idx, 0:d] = curr_id
        curr_id += 1
        in_memory = False
    else:
        memory_new[idx, 0:d] = -1
        free_space[idx] = d
        in_memory = True


for i in tqdm(range(len(memory_new)-1, -1, -1)):
    if (all(memory_new[i] < 0)):
        # Nothing to transfer
        continue
    if (len(set(memory_new[i][memory_new[i] > 1])) > 1):
        # Already transfered
        continue
    j = 0
    length_needed = sum(memory_new[i] > 0)
    while i > j:
        # Check free space (indicated by -1)
        free_space = sum(memory_new[j] == -1)
        if free_space >= length_needed:
            # Transfer whole block.
            # Find index of first -1
            j_idx = np.argwhere(memory_new[j] == -1)[0][0]
            memory_new[j, j_idx:j_idx +
                       length_needed] = memory_new[i, 0:length_needed]
            memory_new[i, 0:length_needed] = -1
            break
        else:
            j += 1


mem = memory_new[memory_new > -2]
mem_mult = np.arange(len(mem))
mem[mem == -1] = 0
print(sum(mem*mem_mult))
