# part 1
# First, treat Map as 2D array and solve recursively.
# Might make part2 too tough to solve if I build a graph

# class Node:
#     def __init__(self, val):
#         self.val = val
import time
class Map:
    def __init__(self, inp):
        self.inp = [line.strip() for line in inp]
        self.R = len(self.inp)
        self.C = len(self.inp[0])
    def __getitem__(self, tup):
        r, c = tup
        assert r >= 0 and r < self.R
        assert c >= 0 and c < self.C
        return self.inp[r][c]
    def get_trailheads(self):
        coords = []
        for r, line in enumerate(self.inp):
            for c, char in enumerate(line):
                if char == '0':
                    coords.append((r, c))
        return coords
    def get_valid_neighbors(self, tup):
        val = self[tup]
        assert int(val) >= 0 and int(val) <= 9, f"Expected int in range 0..10 but got {val}"
        # Climb the hill
        up = str(int(val) + 1)
        next_valids = []
        for r in [-1, 1]:
            rr = tup[0]+r
            cc = tup[1]
            try:
                if self[rr, cc] == up:
                    next_valids.append((rr,cc))
            except:
                pass
        for c in [-1, 1]:
            rr = tup[0]
            cc = tup[1]+c
            try:
                if self[rr, cc] == up:
                    next_valids.append((rr, cc))
            except:
                pass
        return next_valids
    
    def print_cur(self, tup):
        # Print a * at tup
        grid = [['.' for _ in range(self.C)] for _ in range(self.R)]
        for r in range(self.R):
            for c in range(self.C):
                grid[r][c] = self[r,c]
        grid[tup[0]][tup[1]] = '*'
        print('\n'.join([''.join(line) for line in grid]))

def visit(m, cur, ends):
    # m.print_cur(cur)
    # time.sleep(.2)
    # If cur == 9, return True
    if m[cur] == '9':
        # return [cur]
        ends.add(cur)
    # For neighbor in neighbors, visit them
    # for next_valid in map.get_valid_neighbors(cur):
    # return sum(list(map(lambda n: visit(m, n), m.get_valid_neighbors(cur))))
    for next_valid in m.get_valid_neighbors(cur):
        visit(m, next_valid, ends)

    return len(ends)
    # return 0 # Tail condition
    

def p1(input):
    m = Map(open(input).readlines())
    heads = m.get_trailheads()
    print(heads)
    total = 0
    for h in heads:
        ends = set()
        res = visit(m, h, ends)
        # print(f'Starting head {h} achieves {res} trailheads')
        total += res
    print(total)


p1('input.txt')

# Accidentally solved p2 first
def visit(m, cur):
    # m.print_cur(cur)
    # time.sleep(.2)
    # If cur == 9, return True
    if m[cur] == '9':
        return 1
    # For neighbor in neighbors, visit them
    return sum(list(map(lambda n: visit(m, n), m.get_valid_neighbors(cur))))

    return 0 # Tail condition

def p2(input):
    m = Map(open(input).readlines())
    heads = m.get_trailheads()
    print(heads)
    total = 0
    for h in heads:
        res = visit(m, h)
        # print(f'Starting head {h} achieves {res} trailheads')
        total += res
    print(total)

p2('input.txt')