import tqdm
from functools import cache

data = open('input.txt', 'r').read()
data = data.split(' ')

# @cache
def change_stone(s):
    if s == '0':
        return ['1']
    elif len(s)%2==0:
        part = len(s)//2
        return [s[:part], str(int(s[part:]))]
    else:
        return [str(int(s)*2024)]


def blink(stones):
    stones_new = []
    for s in stones:
        stones_new +=change_stone(s)
    return stones_new

stones = data

for i in range(25):
    stones = blink(stones)

print(len(stones))

for i in tqdm.tqdm(range(50)):
    stones = blink(stones)
    

