from sympy import symbols, Eq, solve
import re
import tqdm

buttons_A = []
buttons_B = []
prizes = []

button_match = re.compile('X\+(\d+).*Y\+(\d+)')
prize_match = re.compile('X\=(\d+).*Y\=(\d+)')
with open('input.txt', 'r') as f:
    for line in f.readlines():
        if 'Button A' in line:
            match = button_match.findall(line)[0]
            buttons_A.append((int(match[0]), int(match[1])))
        elif 'Button B' in line:
            match = button_match.findall(line)[0]
            buttons_B.append((int(match[0]), int(match[1])))
        elif 'Prize' in line:
            match = prize_match.findall(line)[0]
            prizes.append((int(match[0]), int(match[1])))


score = 0
for A, B, p in zip(buttons_A, buttons_B, prizes):
    x, y = symbols('x y', integer=True)
    eq1 = Eq(A[0]*x+B[0]*y, p[0])
    eq2 = Eq(A[1]*x+B[1]*y, p[1])
    solution = solve((eq1, eq2), (x, y))
    if solution:
        score += solution[x]*3+solution[y]
print(score)


# second part

score = 0
for A, B, p in zip(buttons_A, buttons_B, prizes):
    x, y = symbols('x y', integer=True)
    eq1 = Eq(A[0]*x+B[0]*y, p[0]+10000000000000)
    eq2 = Eq(A[1]*x+B[1]*y, p[1]+10000000000000)
    solution = solve((eq1, eq2), (x, y))
    if solution:
        score += solution[x]*3+solution[y]
print(score)
