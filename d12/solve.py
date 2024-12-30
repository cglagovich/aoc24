'''
Minimal solution to d12.
'''

def get_all_regions(inp, R, C):
    '''
    Return list of sets of region points.
    For each point, visit it if not in visited. Add it to the current region
    '''
    all_regions = []
    dirs = [1, -1, 1j, -1j]
    visited = set()
    for r in range(R):
        for c in range(C):
            start_pos = complex(r, c)
            q = [start_pos]
            cur_reg_val = inp[int(start_pos.real)][int(start_pos.imag)]
            cur_region = set()
            while len(q) > 0:
                coord = q.pop(0)
                if coord in visited:
                    continue
                visited.add(coord)
                cur_region.add(coord)
                for ndir in dirs:
                    ncoord = coord + ndir
                    # Bounds check
                    if ncoord.real < 0 or ncoord.real >= R or ncoord.imag < 0 or ncoord.imag >= C:
                        continue
                    nval = inp[int(ncoord.real)][int(ncoord.imag)]
                    if nval == cur_reg_val:
                        q.append(ncoord)
            if len(cur_region) > 0:
                all_regions.append(cur_region)
    return all_regions

def get_area(region):
    return len(region)

def get_perimeter(region, R, C):
    perim = 0
    for coord in region:
        # 4 - number of neighbors in region
        n_neighbors = 0
        for ndir in [1, -1, 1j, -1j]:
            ncoord = coord + ndir
            if ncoord in region:
                n_neighbors += 1
        perim += 4 - n_neighbors
    return perim

def get_sides(region):
    '''
    Return the number of sides this region shape has.
    Count the number of corners of the shape. This equals the number of sides
    Need to include convex corners and concave corners.
    '''
    dirs = [1, 1j, -1, -1j]
    dirs_rotated = dirs[1:] + dirs[:1]
    n_corners = 0
    for coord in region:
        for ndir1, ndir2 in zip(dirs, dirs_rotated):
            ncoord1 = coord + ndir1
            ncoord2 = coord + ndir2
            if ncoord1 not in region and ncoord2 not in region:
                # External corner
                n_corners += 1
            corner = coord + ndir1 + ndir2
            if ncoord1 in region and ncoord2 in region and corner not in region:
                # Internal corner
                n_corners += 1
    return n_corners

def solvep1(inp):
    '''
    Sum (area * perimeter) for each region in the space
    '''
    R = len(inp)
    C = len(inp[0])
    regions = get_all_regions(inp, R, C)
    ret = 0
    for reg in regions:
        ret += get_area(reg) * get_perimeter(reg, R, C)
    return ret

def solvep2(inp):
    '''
    Sum (area * sides) for each region in the space
    '''
    R = len(inp)
    C = len(inp[0])
    regions = get_all_regions(inp, R, C)
    ret = 0
    for reg in regions:
        area = get_area(reg)
        sides = get_sides(reg)
        ret += area * sides
    return ret
    
    

import sys
fname = sys.argv[1]
inp = open(fname).readlines()
inp = [i.strip() for i in inp]

print('part 1:', solvep1(inp))
print('part 2:', solvep2(inp))