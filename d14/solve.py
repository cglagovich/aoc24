# part 1
'''
Brute force to start
'''
from collections import namedtuple
XY = namedtuple('XY', ['x', 'y'])

class Robot:
    def __init__(self, p, v, bound):
        self.p = p
        self.v = v
        self.bound = bound
    def step(self):
        new_x = self.p.x + self.v.x
        new_x = new_x % self.bound.x
        new_y = self.p.y + self.v.y
        new_y = new_y % self.bound.y
        self.p = XY(new_x, new_y)
    def __repr__(self):
        return f'Robot(p={self.p}, v={self.v}, bound={self.bound})'

def print_robots(robots):
    bound = robots[0].bound
    grid = [['.' for _ in range(bound.x)] for _ in range(bound.y)]
    for r in robots:
        loc = r.p
        if grid[loc.y][loc.x] != '.':
            grid[loc.y][loc.x] = str(int(grid[loc.y][loc.x])+1)
        else:
            grid[loc.y][loc.x] = "1"
    grid_str = '\n'.join([''.join(row) for row in grid])
    print(grid_str)
    return grid_str

def count_per_quad(robots):
    def get_quad(p, bound):
        half_x = bound.x // 2 + 1
        half_y = bound.y // 2 + 1
        x_part = 1 if p.x >= half_x else 0
        y_part = 1 if p.y >= half_y else 0
        quad = x_part + y_part * 2
        return int(quad)
    bound = robots[0].bound
    quads = [0] * 4
    for robot in robots:
        if robot.p.x == bound.x // 2 or robot.p.y == bound.y // 2:
            continue
        q = get_quad(robot.p, bound)
        quads[q] += 1
    res = 1
    print(quads)
    for q in quads:
        res *= q
    return res

fname = 'input.txt'
# bound = XY(11, 7) # TODO: change for real input
bound = XY(101, 103)
n_steps = 100
lines = open(fname).readlines()
robots = []
for l in lines:
    p, v = l.strip().split('v=')
    p = p[2:].strip().split(',')
    v = v.strip().split(',')
    p = XY(*(int(val) for val in p))
    v = XY(*(int(val) for val in v))
    robot = Robot(p, v, bound)
    robots.append(robot)
# print(robots)

print("Start")
print_robots(robots)
for s in range(n_steps):
    for robot in robots:
        robot.step()
    
    print(f'Step {s}')
    print_robots(robots)


res = count_per_quad(robots)
print(res)



# part 2
fname = 'input.txt'
# bound = XY(11, 7) # TODO: change for real input
bound = XY(101, 103)
n_steps = 100000
lines = open(fname).readlines()
robots = []
for l in lines:
    p, v = l.strip().split('v=')
    p = p[2:].strip().split(',')
    v = v.strip().split(',')
    p = XY(*(int(val) for val in p))
    v = XY(*(int(val) for val in v))
    robot = Robot(p, v, bound)
    robots.append(robot)
# print(robots)

print("Start")
print_robots(robots)
for s in range(n_steps):
    for robot in robots:
        robot.step()
    
    print(f'Step {s}')
    robot_str = print_robots(robots)
    if "1111111" in robot_str:
        breakpoint()


res = count_per_quad(robots)
print(res)