

import sys
fname = sys.argv[1]
locks = []
keys = []

def parse_heights(inp):
    '''
    For each column, add 1 if the row contains a # in that column
    '''
    heights = [0] * len(inp[0])
    for row in inp:
        for c in range(len(row)):
            if row[c] == '#':
                heights[c] += 1
    return tuple(heights)

def fits(key, lock):
    res = map(lambda x: x[0]+x[1], zip(key, lock))
    return all(r <= 5 for r in res)

def solvep1(keys, locks):
    '''
    BRUTE FORCE IT!!!
    '''
    nfits = 0
    for key in keys:
        for lock in locks:
            if fits(key, lock):
                nfits += 1
    return nfits

inpfile = open(fname).read()
for inp in inpfile.split('\n\n'):
    inplines = inp.strip().split('\n')
    if all(inpchar == '#' for inpchar in inplines[0].strip()):
        inpheights = inplines[1:]
        is_lock = True
    else:
        inpheights = inplines[:-1]
        is_lock = False
    heights = parse_heights(inpheights)
    locks.append(heights) if is_lock else keys.append(heights)

print(f'keys: {keys}')
print(f'locks: {locks}')

print('part 1:', solvep1(keys, locks))
