from matplotlib import pyplot as plt
import numpy as np

data = open('input.txt', 'r').read()
data = data.split('\n')
data = [list(d) for d in data]

EAST = (0, 1)
WEST = (0, -1)
NORTH = (-1, 0)
SOUTH = (1, 0)

reverse = {EAST: WEST,
           WEST: EAST,
           NORTH: SOUTH,
           SOUTH: NORTH}


data = np.array(data)

starting_position = np.where(data == 'S')
end_position = np.where(data == 'E')
end_position = (end_position[0][0], end_position[1][0])
starting_position = (starting_position[0][0], starting_position[1][0])
distances = np.ones_like(data, dtype=int) * 10000000000000000
distances[starting_position] = 0
came_from = np.array([[[None, None, None] for _ in range(data.shape[0])]
                     for _ in range(data.shape[1])])


def lookaround(position, direction, new_dirs, QUEUE, DISTANCES):
    new_position = (position[0] + direction[0], position[1]+direction[1])
    if data[new_position] not in ['#', 'S']:
        new_direction = direction
        if distances[new_position] > distances[position] + 1:
            distances[new_position] = distances[position] + 1
            QUEUE.append((new_position, new_direction))
            DISTANCES.append(distances[new_position])
            came_from[new_position[0]][new_position[1]] = [
                position[0], position[1], reverse[direction]]

    for direction in new_dirs:
        new_position = (position[0] + direction[0], position[1]+direction[1])
        if data[new_position] not in ['#', 'S']:
            new_direction = direction
            if distances[new_position] > distances[position] + 1001:
                distances[new_position] = distances[position] + 1001
                came_from[new_position[0]][new_position[1]] = [
                    position[0], position[1], reverse[direction]]
                QUEUE.append((new_position, new_direction))
                DISTANCES.append(distances[new_position])
    return QUEUE, DISTANCES


QUEUE = [(starting_position, EAST)]
DISTANCES = [0]

while len(QUEUE) > 0:
    distances_min = np.argsort(DISTANCES)[0]
    DISTANCES.pop(distances_min)
    position, direction = QUEUE.pop(distances_min)
    if direction == EAST:
        QUEUE, DISTANCES = lookaround(
            position, direction, [NORTH, SOUTH], QUEUE, DISTANCES)
    elif direction == WEST:
        QUEUE, DISTANCES = lookaround(
            position, direction, [NORTH, SOUTH], QUEUE, DISTANCES)
    elif direction == NORTH:
        QUEUE, DISTANCES = lookaround(
            position, direction, [EAST, WEST], QUEUE, DISTANCES)
    elif direction == SOUTH:
        QUEUE, DISTANCES = lookaround(
            position, direction, [EAST, WEST], QUEUE, DISTANCES)

distances[distances == 10000000000000000] = -1
np.savetxt("out.csv", distances, delimiter=",", fmt="%d")

plt.imshow(distances)
plt.show()

# Second part. Build a collection of paths.
# Go one against one. If you can turn and its the same distance, calculate from that too.
# This time use breadth first search.
# First visual for best path.
NODE = end_position
best_path = np.zeros_like(distances)
QUEUE_TEST = [end_position]
SET_BEST = {tuple(end_position)}
while True:
    if NODE[0] == starting_position[0] and NODE[1] == starting_position[1]:
        break
    best_path[NODE[0]][NODE[1]] = 1
    NODE = [came_from[NODE[0]][NODE[1]][0], came_from[NODE[0]][NODE[1]][1]]
    QUEUE_TEST.append(NODE)
    SET_BEST.add(tuple(NODE))

QUEUE_TEST.pop(0)
while len(QUEUE_TEST) > 0:
    NODE = QUEUE_TEST.pop(0)
    # JUST CHECK ALL COMBOS
    # directions = [EAST, WEST, NORTH, SOUTH]
    dis_here = distances[NODE[0]][NODE[1]]

    # print('NODE distance:', dis_here)

    # print('Neighbour distances:')

    NODE_EAST = (NODE[0]+EAST[0], NODE[1]+EAST[1])
    east_node_dis = distances[NODE_EAST[0]][NODE_EAST[1]]
    NODE_WEST = (NODE[0]+WEST[0], NODE[1]+WEST[1])
    west_node_dis = distances[NODE_WEST[0]][NODE_WEST[1]]

    NODE_SOUTH = (NODE[0]+SOUTH[0], NODE[1]+SOUTH[1])
    south_node_dis = distances[NODE_SOUTH[0]][NODE_SOUTH[1]]
    NODE_NORTH = (NODE[0]+NORTH[0], NODE[1]+NORTH[1])
    north_node_dis = distances[NODE_NORTH[0]][NODE_NORTH[1]]
    if abs(east_node_dis-west_node_dis) == 2 and abs(east_node_dis-dis_here) != 1:
        for N in [NODE_EAST, NODE_WEST]:
            NODE_N = tuple(N)
            while True:
                if NODE_N in SET_BEST:
                    break
                best_path[NODE_N[0]][NODE_N[1]] = 1
                QUEUE_TEST.append(NODE_N)
                SET_BEST.add(tuple(NODE_N))
                NODE_N = (came_from[NODE_N[0]][NODE_N[1]]
                          [0], came_from[NODE_N[0]][NODE_N[1]][1])

    if abs(south_node_dis-north_node_dis) == 2 and abs(south_node_dis-dis_here) != 1:
        for N in [NODE_SOUTH, NODE_NORTH]:
            NODE_N = tuple(N)
            while True:
                if NODE_N in SET_BEST:
                    break
                best_path[NODE_N[0]][NODE_N[1]] = 1
                QUEUE_TEST.append(NODE_N)
                SET_BEST.add(tuple(NODE_N))
                NODE_N = (came_from[NODE_N[0]][NODE_N[1]]
                          [0], came_from[NODE_N[0]][NODE_N[1]][1])

    # for d in directions:
    #     new_node = (NODE[0]+d[0], NODE[1]+d[1])

    #     if distances[new_node[0]][new_node[1]] == -1:
    #         continue

    #     if dis_here-distances[new_node[0]][new_node[1]] == -999:
    #         NODE_N = tuple(new_node)
    #         while True:
    #             if NODE_N in SET_BEST:
    #                 break
    #             best_path[NODE_N[0]][NODE_N[1]] = 1
    #             QUEUE_TEST.append(NODE_N)
    #             SET_BEST.add(tuple(NODE_N))
    #             NODE_N = (came_from[NODE_N[0]][NODE_N[1]]
    #                       [0], came_from[NODE_N[0]][NODE_N[1]][1])

        # if best_path[new_node[0]][new_node[1]] != 1:
        #     SET_BEST.add(new_node)
        #     QUEUE_TEST.append(new_node)
        #     best_path[new_node[0]][new_node[1]] = 1


# Just subtract the wrong loops from answer lol
print(np.sum(best_path)+1)
plt.imshow(best_path)
plt.show()
