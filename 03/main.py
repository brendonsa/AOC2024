import re
import numpy as np

# Read input from input.txt
data = open('input.txt', 'r').read()

# Build regex for finding mul(\d+,\d+)

# Part1


def find_mul(data):
    mul_re = re.compile('mul\((\d+),(\d+)\)')
    find = mul_re.findall(data)
    res = 0
    for f in find:
        l, r = int(f[0]), int(f[1])
        res += l*r
    return res


print(find_mul(data))
# Part2

# Regex for deleting don\'t\(\).*do() sequences
disable_re = re.compile('don\'t\(\).*?do\(\)')
data = data.replace('\n', '')
disable_last = re.compile('don\'t.*')
data_sub = disable_re.sub('', data)
data_sub = disable_last.sub('', data_sub)
print(find_mul(data_sub))


# Eliminate without regex.
mask = np.ones(len(data), dtype=bool)
curr = True
for idx in range(len(data)):
    dont = data[idx:idx+7]
    do = data[idx:idx+4]
    if dont == 'don\'t()':
        curr = False
    elif do == 'do()':
        curr = True
    mask[idx] = curr
data_np = np.array(list(data))
data_sub = data_np[mask]
data_sub = ''.join(data_sub)

print(find_mul(data_sub))
