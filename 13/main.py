from sympy import symbols, Eq, solve
import re
import time
import numpy as np

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
idx = 0
idxes = []
start_time = time.time()
solutions = []
for A, B, p in zip(buttons_A, buttons_B, prizes):
    x, y = symbols('x y', integer=True)
    eq1 = Eq(A[0]*x+B[0]*y, p[0])
    eq2 = Eq(A[1]*x+B[1]*y, p[1])
    solution = solve((eq1, eq2), (x, y))
    if solution:
        idxes.append(idx)
        score += solution[x]*3+solution[y]
        solutions.append(np.array([solution[x], solution[y]]))
    else:
        solutions.append(None)
    idx += 1
print(score)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")


# second part

score = 0
start_time = time.time()

for A, B, p in zip(buttons_A, buttons_B, prizes):
    x, y = symbols('x y', integer=True)
    eq1 = Eq(A[0]*x+B[0]*y, p[0]+10000000000000)
    eq2 = Eq(A[1]*x+B[1]*y, p[1]+10000000000000)
    solution = solve((eq1, eq2), (x, y))
    if solution:
        score += solution[x]*3+solution[y]
print(score)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")


# Faster numpy solution
start_time = time.time()
solutions_np = []
for b_A, b_B, p in zip(buttons_A, buttons_B, prizes):
    A = np.array([[b_A[0], b_B[0]], [b_A[1], b_B[1]]])
    B = np.array([p[0], p[1]])
    X = np.linalg.solve(A, B)
    X_int = np.array(np.round(X), dtype=int)
    if np.all(np.dot(A, X_int) == B):
        solutions_np.append(X_int)

solutions_np = np.array(solutions_np)
print(np.sum(np.dot(solutions_np, np.array([3, 1]))))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")


start_time = time.time()
solutions_np = []
for b_A, b_B, p in zip(buttons_A, buttons_B, prizes):
    A = np.array([[b_A[0], b_B[0]], [b_A[1], b_B[1]]])
    B = np.array([p[0]+10000000000000, p[1]+10000000000000])
    X = np.linalg.solve(A, B)
    X_int = np.array(np.round(X), dtype=int)
    if np.all(np.dot(A, X_int) == B):
        solutions_np.append(X_int)

solutions_np = np.array(solutions_np)
print(np.sum(np.dot(solutions_np, np.array([3, 1]))))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
