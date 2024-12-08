data = open('input.txt', 'r').read()
data = data.split('\n')

test_vals = [int(d.split(':')[0]) for d in data]
numbers = [d.split(':')[1][1:]  for d in data]

def test_first(numbers, res):
    if len(numbers) == 1:
        return numbers[0] == res
    
    passes = False

    if res % numbers[-1] == 0:
        new_res = res // numbers[-1]
        passes = test_first(numbers[:-1], new_res)
    if passes:
        return True
    else:
        new_res = res - numbers[-1]
        passes = test_first(numbers[:-1], new_res)
    
    return passes


count = 0

for t, n in zip(test_vals, numbers):
    n = list(map(int, n.split(' ')))
    if test_first(n, t):
        count+=t

print(count)


def test_second(numbers, res):
    if len(numbers) == 1:
        return numbers[0] == res
    
    passes = False
    last_num = str(numbers[-1])
    if str(res)[-len(last_num):] == last_num:
        try:
            new_res = int(str(res)[:-len(last_num)])
            passes = test_second(numbers[:-1], new_res)
        except:
            pass
    if passes:
        return passes
    if res % numbers[-1] == 0:
        new_res = res // numbers[-1]
        passes = test_second(numbers[:-1], new_res)
    if passes:
        return True
    else:
        new_res = res - numbers[-1]
        passes = test_second(numbers[:-1], new_res)
    
    return passes

count = 0

for t, n in zip(test_vals, numbers):
    n = list(map(int, n.split(' ')))
    if test_second(n, t):
        count+=t

print(count)