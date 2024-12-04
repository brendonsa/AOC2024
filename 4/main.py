from numpy.lib.stride_tricks import sliding_window_view
import numpy as np
import re

data = open('input.txt', 'r').read()
data = data.split('\n')
data = [list(d) for d in data]
data = np.array(data)

DIM = data.shape


def check_in_picture(coords):
    # Check if all coordinates fall in DIM
    return all(0 <= c[0] < DIM[0] for c in coords) and all(0 <= c[1] < DIM[1] for c in coords)


def make_steps(coord, v, h, steps=4):
    coords = [coord]
    for i in range(1, steps):
        coords.append((coord[0] + (i*v), coord[1] + (i*h)))
    if check_in_picture(coords):
        return coords
    else:
        return None


def make_diagonal_dr(coord, steps=4):
    return make_steps(coord, 1, 1, steps)


def make_diagonal_dl(coord, steps=4):
    return make_steps(coord, 1, -1, steps)


def make_diagonal_ur(coord, steps=4):
    return make_steps(coord, -1, 1, steps)


def make_diagonal_ul(coord, steps=4):
    return make_steps(coord, -1, -1, steps)


def make_u(coord, steps=4):
    return make_steps(coord, -1, 0, steps)


def make_d(coord, steps=4):
    return make_steps(coord, 1, 0, steps)


def make_l(coord, steps=4):
    return make_steps(coord, 0, -1, steps)


def make_r(coord, steps=4):
    return make_steps(coord, 0, 1, steps)


def look_arround(coord, steps=4):
    coords_all = []
    coords_all.append(make_l(coord, steps=steps))
    coords_all.append(make_r(coord, steps=steps))
    coords_all.append(make_u(coord, steps=steps))
    coords_all.append(make_d(coord, steps=steps))
    coords_all.append(make_diagonal_dl(coord, steps=steps))
    coords_all.append(make_diagonal_dr(coord, steps=steps))
    coords_all.append(make_diagonal_ul(coord, steps=steps))
    coords_all.append(make_diagonal_ur(coord, steps=steps))
    coords_all = [x for x in coords_all if x is not None]
    return coords_all


def build_string(data, coords):
    string = ''
    for c in coords:
        string += data[c]
    return string


# First part
xmas = 0
for i in range(DIM[0]):
    for j in range(DIM[1]):
        if data[i, j] == 'X':
            coords = look_arround((i, j))
            for c in coords:
                if build_string(data, c) == 'XMAS':
                    xmas += 1

print(xmas)
# Second part


def look_diagonals_from_a(coord):
    coords_all = []
    coords_all.append([(coord[0] - 1, coord[1]-1),
                      (coord[0], coord[1]), (coord[0]+1, coord[1]+1)])
    coords_all.append([(coord[0] + 1, coord[1]-1),
                      (coord[0], coord[1]), (coord[0]-1, coord[1]+1)])
    for c in coords_all:
        if not check_in_picture(c):
            return None
    return coords_all


xmas = 0
for i in range(DIM[0]):
    for j in range(DIM[1]):
        if data[i, j] == 'A':
            coords = look_diagonals_from_a((i, j))
            if coords is None:
                continue
            else:
                if build_string(data, coords[0]) in ['MAS', 'SAM'] and build_string(data, coords[1]) in ['MAS', 'SAM']:
                    xmas += 1
print(xmas)


# Part 1 numpy solution

def count_xmas_in_line(line):
    xmas_re = re.compile(r'XMAS')
    return sum(1 for _ in xmas_re.finditer(line)) + sum(1 for _ in xmas_re.finditer(line[::-1]))


xmas_vertical = sum(count_xmas_in_line(''.join(line)) for line in data)
xmas_horizontal = sum(count_xmas_in_line(''.join(line)) for line in data.T)

xmas_diagonal = sum(count_xmas_in_line(
    ''.join(np.diagonal(data, offset=i))) for i in range(DIM[0]))
xmas_diagonal_minus = sum(count_xmas_in_line(
    ''.join(np.diagonal(data, offset=-i))) for i in range(1, DIM[0]))
xmas_diagonal_r = sum(count_xmas_in_line(
    ''.join(np.diagonal(np.fliplr(data), offset=i))) for i in range(DIM[0]))
xmas_diagonal_r_minus = sum(count_xmas_in_line(
    ''.join(np.diagonal(np.fliplr(data), offset=-i))) for i in range(1, DIM[0]))

print(sum((xmas_vertical, xmas_horizontal, xmas_diagonal,
      xmas_diagonal_minus, xmas_diagonal_r, xmas_diagonal_r_minus)))

# Part 2 numpy solution


window_shape = (3, 3)
windows = sliding_window_view(data, window_shape)
xmas = 0
for i in range(windows.shape[0]):
    for j in range(windows.shape[1]):
        # Extract the 3x3 window
        w = windows[i, j]
        if ''.join(np.diag(w)) in ['MAS', 'SAM'] and ''.join(np.diag(np.fliplr(w))) in ['MAS', 'SAM']:
            xmas += 1
print(xmas)
