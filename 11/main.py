import tqdm
from functools import lru_cache

data = open('input.txt', 'r').read()
data = data.split(' ')
data = list(map(int, data))


@lru_cache(maxsize=None)
def change_stone(s):
    if s == 0:
        return [1]
    elif len(str(s)) % 2 == 0:
        part = len(str(s))//2
        return [int(str(s)[:part]), int(str(s)[part:])]
    else:
        return [s*2024]


def blink(stones):
    stones_new = []
    for s in stones:
        stones_new += change_stone(s)
    return stones_new


@lru_cache(maxsize=None)
def blink_r(stone, depth):
    count = 0
    if depth == 1:
        s = change_stone(stone)
        count += len(s)
        return count
    else:
        stones = change_stone(stone)
        for s in stones:
            count += blink_r(s, depth-1)
    return count


stones = data

count = 0
for s in stones:
    count += blink_r(s, 25)

print(count)

count = 0
for s in stones:
    count += blink_r(s, 75)

print(count)
