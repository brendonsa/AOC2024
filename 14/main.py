import re
import numpy as np
from matplotlib import pyplot as plt

WIDTH = 101
HEIGHT = 103


class Robot():
    def __init__(self, pos, velocities):
        self.x = pos[0]
        self.y = pos[1]
        self.v_x = velocities[0]
        self.v_y = velocities[1]

    @property
    def pos(self):
        return [self.x,self.y]
    
    def walk(self):
        self.x = (self.x + self.v_x) % WIDTH
        self.y = (self.y + self.v_y) % HEIGHT
    

data = open('input.txt', 'r').read()
data = data.split('\n')
robot_re = re.compile('p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)')
robots = []
for d in data:
    x = int(robot_re.match(d).groups()[0])
    y = int(robot_re.match(d).groups()[1])
    v_x = int(robot_re.match(d).groups()[2])
    v_y = int(robot_re.match(d).groups()[3])
    robots.append(Robot([x,y],[v_x,v_y]))


for i in range(100):
    positions = np.zeros((HEIGHT,WIDTH),dtype=int)
    for r in robots:
        r.walk()
        positions[r.pos[1],r.pos[0]]+=1
    # plt.imshow(positions)
    # plt.savefig(f'./{i}.png')
    # plt.show()

positions = np.zeros((HEIGHT,WIDTH),dtype=int)

for r in robots:
    positions[r.pos[1],r.pos[0]]+=1


w = WIDTH//2
h = HEIGHT//2

q1 = positions[:h,:w].sum()
q2 = positions[-h:,:w].sum()
q3 = positions[:h,-w:].sum()
q4 = positions[-h:,-w:].sum()

print(q1*q2*q3*q4)


for i in range(100000):
    positions = np.zeros((HEIGHT,WIDTH),dtype=int)
    for r in robots:
        r.walk()
        positions[r.pos[1],r.pos[0]]+=1
    if not np.any(positions>1):
        # Visually. I suppose that the puzzle was done by firstly building the christmas tree
        # It should be non overlapping so just check the non overlapping images
        plt.imshow(positions)
        plt.savefig(f'./{i+101}.png')
        print(i+101)
        break
