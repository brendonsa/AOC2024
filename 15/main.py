import numpy as np
from matplotlib import pyplot as plt

EAST = (0, 1)
WEST = (0, -1)
NORTH = (-1, 0)
SOUTH = (1, 0)

directions = {'>':EAST,
              '^':NORTH,
              'v':SOUTH,
              '<':WEST}

warehouse = open('map.txt', 'r').read()
warehouse = warehouse.split('\n')
warehouse = [list(w) for w in warehouse]


starting_position = (0,0)
for idx, w in enumerate(warehouse):
    for jdx, w_ in enumerate(w):
        if w_ == '@':
            starting_position = (idx,jdx)


instructions = open('instructions.txt', 'r').read()
instructions = instructions.replace('\n','')
instructions = list(instructions)


def push(warehouse, position, direction):
    new_position = (position[0]+direction[0],position[1]+direction[1])
    new_element = warehouse[new_position[0]][new_position[1]]
    if new_element == '#':
        return False
    else:
        if new_element == 'O':
            pushed = push(warehouse,new_position,direction)
            if pushed :
                warehouse[position[0]][position[1]], warehouse[new_position[0]][new_position[1]] = warehouse[new_position[0]][new_position[1]], warehouse[position[0]][position[1]]
                return True
        elif new_element == '.':
            warehouse[position[0]][position[1]], warehouse[new_position[0]][new_position[1]] = warehouse[new_position[0]][new_position[1]], warehouse[position[0]][position[1]]
            return True
        elif new_element in '[]':
            assert(direction in [EAST,WEST])
            pushed = push(warehouse,new_position,direction)
            if pushed :
                warehouse[position[0]][position[1]], warehouse[new_position[0]][new_position[1]] = warehouse[new_position[0]][new_position[1]], warehouse[position[0]][position[1]]
                return True
        
position = starting_position
for i in instructions:
    direction = directions[i]
    pushed = push(warehouse,position,direction)
    if pushed:
        position = (position[0]+direction[0],position[1]+direction[1])

score = 0

for idx, w in enumerate(warehouse):
    for jdx, w_ in enumerate(w):
        if w_ == 'O':
            score += idx*100 + jdx

print(score)

# PUSH WIDE. Check where from you are pushing. If you are pushing from/to l/r apply the usual push procedure.
# Pushing from/to t/b should try to apply LOGICAL AND operation for [] except when pushing self (@)


def can_push_wide(warehouse,position,direction):
    new_position = (position[0]+direction[0],position[1]+direction[1])
    new_element = warehouse[new_position[0]][new_position[1]]

    if new_element == '[':
        position_r = (new_position[0],new_position[1]+1)
        return can_push_wide(warehouse,new_position,direction) and can_push_wide(warehouse,position_r,direction)
    elif new_element == ']':
        position_l = (new_position[0],new_position[1]-1)
        return  can_push_wide(warehouse,new_position,direction) and can_push_wide(warehouse,position_l,direction)
    elif new_element == '#':
        return False
    elif new_element == '.':
        return True


def push_wide(warehouse,position, direction):
    new_position = (position[0]+direction[0],position[1]+direction[1])
    new_element = warehouse[new_position[0]][new_position[1]]
    if new_element == '#':
        return False
    else:
        if new_element == '[':
            position_r = (position[0],position[1]+1)
            new_position_r = (position_r[0]+direction[0],position_r[1]+direction[1])
            if can_push_wide(warehouse,new_position,direction) and can_push_wide(warehouse,new_position_r,direction):
                push_wide(warehouse,new_position,direction)
                warehouse[position[0]][position[1]], warehouse[new_position[0]][new_position[1]] = warehouse[new_position[0]][new_position[1]], warehouse[position[0]][position[1]]
                push_wide(warehouse,new_position_r,direction)
                return True
        elif new_element == ']':
            position_l = (position[0],position[1]-1)
            new_position_l = (position_l[0]+direction[0],position_l[1]+direction[1])
            if can_push_wide(warehouse,new_position,direction) and can_push_wide(warehouse,new_position_l,direction):
                push_wide(warehouse,new_position,direction)
                warehouse[position[0]][position[1]], warehouse[new_position[0]][new_position[1]] = warehouse[new_position[0]][new_position[1]], warehouse[position[0]][position[1]]
                position_l = (position[0],position[1]-1)
                new_position_l = (position_l[0]+direction[0],position_l[1]+direction[1])
                push_wide(warehouse,new_position_l,direction)
                return True
        elif new_element == '.':
            warehouse[position[0]][position[1]], warehouse[new_position[0]][new_position[1]] = warehouse[new_position[0]][new_position[1]], warehouse[position[0]][position[1]]
            return True
        
warehouse = open('map.txt', 'r').read()
warehouse = warehouse.replace('#','##').replace('O','[]').replace('.','..').replace('@','@.')
warehouse = warehouse.split('\n')
warehouse = [list(w) for w in warehouse]

starting_position = (0,0)
for idx, w in enumerate(warehouse):
    for jdx, w_ in enumerate(w):
        if w_ == '@':
            starting_position = (idx,jdx)
position = starting_position
for i in instructions:
    direction = directions[i]
    if direction in [EAST,WEST]:
        
        pushed = push(warehouse,position,direction)
    else:
        pushed = push_wide(warehouse,position,direction)
    if pushed:
        position = (position[0]+direction[0],position[1]+direction[1])


score = 0

for idx, w in enumerate(warehouse):
    for jdx, w_ in enumerate(w):
        if w_ == '[':
            score += idx*100 + jdx

print(score)