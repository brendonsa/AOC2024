import re
from functools import lru_cache

data = open('input.txt', 'r').read()
data = data.split('\n')
towels = open('towels.txt', 'r').read()
towels = towels.replace(' ', '').split(',')


@lru_cache(maxsize=None)
def test_string(s):
    for t in towels:
        length = len(t)
        substring = s[0:length]
        if substring == t:
            if s[length:] == '':
                return True
            else:
                if test_string(s[length:]):
                    return True
    return False


a = 0
viable = []
for d in data:
    if test_string(d):
        a += 1
        viable.append(d)
print(a)


@lru_cache(maxsize=None)
def count_variants(s):
    to_return = 0
    for t in towels:
        length = len(t)
        substring = s[0:length]
        if substring == t:
            if s[length:] == '':
                to_return += 1
            else:
                to_return += count_variants(s[length:])
    return to_return


a = 0
for d in viable:
    var = count_variants(d)
    a += count_variants(d)
print(a)
