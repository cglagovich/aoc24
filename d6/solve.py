# part 1
lines = open("input.txt").readlines()

deltas = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1)}
n_dir = {'v': '<', '<': '^', '^': '>', '>': 'v'}


class Map:
    def __init__(self, l):
        self.l = [ll.strip() for ll in l]
        self.R = len(self.l)
        self.C = len(self.l[0])
    def __getitem__(self, tup):
        assert len(tup) == 2
        if tup[0] < 0 or tup[0] >= self.R or tup[1] < 0 or tup[1] >= self.C:
            raise IndexError
        # assert tup[0] >= 0 and tup[0] <= self.R
        # assert tup[1] >= 0 and tup[1] <= self.C
        return self.l[tup[0]][tup[1]]
    def guard_state(self):
        for rdx, row in enumerate(self.l):
            for d in deltas.keys():
                if d in row:
                    return (rdx, row.index(d)), d
    def is_empty(self, tup):
        return self[tup] == '.'
    
    def get_with_obstr(self, tup, obstr):
        if tup == obstr:
            return '#'
        return self[tup]
    def to_str(self, obstr, points):
        grid = [list(row.strip()) for row in self.l]
        for gpp, _ in points:
            grid[gpp[0]][gpp[1]] = 'X'
        grid[obstr[0]][obstr[1]] = 'O'
        start, _ = self.guard_state()
        grid[start[0]][start[1]] = self[start]

        return '\n'.join(''.join(l) for l in grid)

    
m = Map(lines)

gp = set()
# Follow the guard path and add visited points to the set
gpos, gs = m.guard_state()
print(gpos, gs)
while 1:
    gp.add(gpos)
    try:
        d = deltas[gs]
        next_spot = gpos[0] + d[0], gpos[1] + d[1]
        if m[next_spot] != '#':
            gpos = next_spot
        else:
            gs = n_dir[gs]
    except:
        break

# Pretty print all positions the guard encountered
grid = [list(row.strip()) for row in lines]
for gpp in gp:
    grid[gpp[0]][gpp[1]] = 'X'

print('\n'.join(''.join(l) for l in grid))

print(len(gp))
    

# part 2
# Big outer loop where I put an obstruction in each position
res = 0
import tqdm
for nr in tqdm.tqdm(range(m.R)):
    for nc in range(m.C):
        obstr = (nr, nc)
        # print(obstr)
        if not m.is_empty(obstr):
            continue
        gp = set()
        # Follow the guard path and add visited points to the set
        gpos, gs = m.guard_state()

        while 1:
            if (gpos, gs) in gp:
                res += 1 # Found a loop! Find out how to print this later
                print(f'obstr: {obstr}')
                s = m.to_str(obstr, gp)
                print(s)
                break
            gp.add((gpos, gs))
            try:
                d = deltas[gs]
                next_spot = gpos[0] + d[0], gpos[1] + d[1]
                if m.get_with_obstr(next_spot, obstr) != '#':
                    gpos = next_spot
                else:
                    gs = n_dir[gs]
            except:
                break

print(res)
