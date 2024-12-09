from collections import defaultdict

class Coord:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __add__(self, coord):
        return Coord(self.r + coord.r, self.c + coord.c)
    
    def __sub__(self, coord):
        return Coord(self.r - coord.r, self.c - coord.c)
    
    def in_bounds(self, R, C):
        return self.r >= 0 and self.c >= 0 and self.r < R and self.c < C

    def __repr__(self):
        return f'Coord(r={self.r}, c={self.c})'
    
    def __eq__(self, rhs):
        return self.r == rhs.r and self.c == rhs.c
    
    def __hash__(self):
        return hash((self.r, self.c))
    
def pretty(m, antis):
    grid = [['.' for _ in range(len(m[0]))] for _ in range(len(m))]
    for rdx in range(len(m)):
        for cdx in range(len(m[0])):
            grid[rdx][cdx] = m[rdx][cdx]
            if Coord(rdx, cdx) in antis:
                grid[rdx][cdx] = '#'
    
    return '\n'.join(''.join(g) for g in grid)

# part 1
file = "input.txt"
# build mapping of freq -> list of coords
m = [s.strip() for s in open(file).readlines()]
freqs = defaultdict(list)
for rdx, line in enumerate(m):
    for cdx, val in enumerate(line):
        if val != '.':
            freqs[val].append(Coord(rdx, cdx))

# compute pairwise distances between same type antennas
# apply that distance to each antenna to find antinodes
# track those antinodes and pretty print
R = len(m)
C = len(m[0])

antis = set()

for ant, coords in freqs.items():
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            a0 = coords[i]
            a1 = coords[j]
            d = a1 - a0
            # d = (a1[0] - a0[0], a1[1] - a0[1])
            print(f'{a1} - {a0} = {d}')

            ant1 = a1 + d
            ant0 = a0 - d
            if ant1.in_bounds(R, C):
                antis.add(ant1)
            if ant0.in_bounds(R, C):
                antis.add(ant0)

# print(pretty(m, antis))
# print(antis)
print(len(antis))


R = len(m)
C = len(m[0])

antis = set()

for ant, coords in freqs.items():
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            a0 = coords[i]
            a1 = coords[j]
            d = a1 - a0
            # d = (a1[0] - a0[0], a1[1] - a0[1])
            print(f'{a1} - {a0} = {d}')

            ant1 = a1
            antis.add(ant1) # If in pair, self is antinode
            ant0 = a0
            antis.add(ant0) # If in pair, self is antinode
            while (ant1:=ant1 + d).in_bounds(R,C):
                antis.add(ant1)
            while (ant0:=ant0 - d).in_bounds(R,C):
                antis.add(ant0)

print(pretty(m, antis))
print(antis)
print(len(antis))