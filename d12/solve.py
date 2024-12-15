class Map:
    def __init__(self, inp):
        self.inp = [line.strip() for line in inp]
        self.R = len(self.inp)
        self.C = len(self.inp[0])
    def __getitem__(self, tup):
        if isinstance(tup, Coord):
            tup = (tup.r, tup.c)
        r, c = tup
        assert r >= 0 and r < self.R
        assert c >= 0 and c < self.C
        return self.inp[r][c]
    def print(self):#, tup):
        # Print a * at tup
        grid = [['.' for _ in range(self.C)] for _ in range(self.R)]
        for r in range(self.R):
            for c in range(self.C):
                grid[r][c] = self[r,c]
        # grid[tup[0]][tup[1]] = '*'
        print('\n'.join([''.join(line) for line in grid]))

    def iter_coords(self):
        for r in range(self.R):
            for c in range(self.C):
                yield (r, c)

    def get_valid_neighbors(self, tup):
        val = self[tup]
        # Climb the hill
        next_valids = []
        for r in [-1, 1]:
            rr = tup[0]+r
            cc = tup[1]
            try:
                if self[rr, cc] == val:
                    next_valids.append((rr,cc))
            except:
                pass
        for c in [-1, 1]:
            rr = tup[0]
            cc = tup[1]+c
            try:
                if self[rr, cc] == val:
                    next_valids.append((rr, cc))
            except:
                pass
        return next_valids
    
    def get_sides(self, tup):
        '''
        Returns the sides for this plant idx.
        
        XXXX
        XXOX
        XXOO
        XXXX

        Note that the top O has a Side(NS, (1, 2), (2, 2), start_mergeable=False)
        It is important to capture the mergeability of a side upon its creation.
        '''
        # Handle edge cases

        this_plant = self[tup]
        sides = set()
        co = Coord(*tup)
        if co.r == 0:
            sides.add(Side(dir='WE', start=co, end=co+(0,1)))
        if co.r == self.R - 1:
            sides.add(Side(dir='WE', start=co+(1,0), end=co+(1,1)))
        if co.c == 0:
            sides.add(Side(dir='NS', start=co, end=co+(1,0)))
        if co.c == self.C - 1:
            sides.add(Side(dir='NS', start=co+(0,1), end=co+(1,1)))
        
        adjs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for adj in adjs:
            try:
                val = self[co+adj]
                if val != this_plant:
                    # This is a side!
                    if adj == (1, 0):
                        dir = 'WE'
                        start =  co + (1, 0)
                        end = co + (1, 1)
                    elif adj == (-1, 0):
                        dir = 'WE'
                        start = co
                        end = co + (0, 1)
                    elif adj == (0, 1):
                        dir = 'NS'
                        start = co + (0, 1)
                        end = co + (1, 1)
                    elif adj == (0, -1):
                        dir = 'NS'
                        start = co
                        end = co + ((1, 0))
                    else:
                        assert False
                    sides.add(Side(dir, start, end))
                    pass
            except:
                # out of bounds, do nothing
                pass
        return sides

class Coord:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    def __add__(self, rhs):
        if not isinstance(rhs, Coord):
            rhs = Coord(*rhs)
        return Coord(self.r+rhs.r, self.c+rhs.c)
    def __neg__(self):
        return Coord(-self.r, -self.c)
    def t(self):
        return Coord(self.c, self.r)
    def __repr__(self):
        return f'Coord(r={self.r}, c={self.c})'
    def __eq__(self, rhs):
        return self.r == rhs.r and self.c == rhs.c
    def __hash__(self):
        return hash((self.r, self.c))

from collections import namedtuple
Side = namedtuple('side', ['dir', 'start', 'end', 'start_mergeable', 'end_mergeable'], defaults=[True, True])


# part 1
"""
For each region, calculate the perimeter (number of sides not adjacent to a plant of the same type)
and the area (total number of plants in the region).

This can be done in one pass. First, discover the region by traversing. Once a region is fully discovered, calculate
its perimeter and area and add that to the result.

Keep track of visited points.

"""
m = Map(open('input.txt').readlines())

visited = set()
# cur_area = 0
# cur_perim = 0
cur_plant = None

def visit(tup):
    # print(f'visiting m[{tup}]={m[tup]}')
    # Return value is (area, perimeter)
    # tup should never have been visited before
    assert tup not in visited
    visited.add(tup)
    neighbors = m.get_valid_neighbors(tup)

    res = (1, 4-len(neighbors))
    
    for n in neighbors:
        if n not in visited:
            n_val = visit(n)
            res = (res[0] + n_val[0], res[1] + n_val[1])
            # print(res)
    return res

ret = 0
for tup in m.iter_coords():
    if tup in visited:
        continue
    area, perim = visit(tup)
    ret += area * perim

print(ret)


# part 2
m = Map(open('sample4.txt').readlines())

visited = set()
# cur_area = 0
# cur_perim = 0
cur_plant = None

def visit(tup):
    # print(f'visiting m[{tup}]={m[tup]}')
    # Return value is (area, perimeter)
    # tup should never have been visited before
    assert tup not in visited
    visited.add(tup)
    neighbors = m.get_valid_neighbors(tup)

    res = (1, 4-len(neighbors))
    
    for n in neighbors:
        if n not in visited:
            n_val = visit(n)
            res = (res[0] + n_val[0], res[1] + n_val[1])
    return res

def n_sides(nodes):
    """
    From a set of nodes which create a contiguous region, find the number of edges of the shape it creates
    OOOOO
    OXOXO
    OOOOO
    OXOXO
    OOOOO

    RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE
    
    Alg:
    Iterate over the set of nodes. If the node has 4 neighbors, it's an interior node so it should be skipped.
    Build a set of edges.
    For each node, find the coords in which it doesn't have neighbors.
    Find the edge that 

    Alt alg:
    Build a set of sides. A side is a direction (N/S or E/W) and a coordinate (r, c). 
    Edge (N/S, (0,0), (1,0)) is the edge to the left of the first element.
    """

    sides = set()
    for n in nodes:
        sides |= m.get_sides(n)

    # print(f'{sides=}')

    # Now we have the set of sides!
    # Iteratively merge
    prev = sides
    merge_step = 0
    while True:
        print(f'merge step {merge_step}')
        skip = set()
        merged = set()
        for s in prev:
            if s in skip:
                continue
            for ss in prev - (skip | set([s])):
                if s.dir != ss.dir:
                    continue
                # breakpoint()
                if s.end == s.start:
                    merged.add(Side(s.dir, s.start, ss.end))
                    skip.add(s)
                    skip.add(ss)
                    break
                if s.start == ss.end:
                    merged.add(Side(s.dir, ss.start, s.end))
                    skip.add(s)
                    skip.add(ss)
                    break
        # print(f'{merged=}')
        # print(f'{skip=}')
        merged = merged | (prev - skip)
        if len(merged) == len(prev):
            # No more merging can be done
            break
        prev = merged
        merge_step += 1


    return len(prev)



    

ret = 0
for tup in m.iter_coords():
    if tup in visited:
        continue
    prev_visited = visited.copy()
    area, perim = visit(tup)
    # ret += area * perim
    cur_plants = visited - prev_visited
    plant_sides = n_sides(cur_plants)
    print(f'{m[tup]}: {plant_sides}')
    ret += area * plant_sides


print(ret)

# TODO: This is buggy for sample 4, where the edges are mistakenly merged.
