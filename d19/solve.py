import sys
fname = sys.argv[1]
opts, patterns = open(fname).read().split('\n\n')
opts = [o.strip() for o in opts.strip().split(',')]
patterns = patterns.strip().split('\n')

def construct(opts, pattern):
    '''
    DFS to find any pattern which works
    '''
    visited = set()
    q = [0] # Holds start idx of pattern left to consume
    while len(q) > 0:
        pat_idx = q.pop()
        if pat_idx == len(pattern):
            return 1
        for opt in opts:
            if pattern[pat_idx:].startswith(opt):
                upto = pat_idx+len(opt)
                if upto not in visited:
                    q.append(upto)
                    visited.add(upto)
        
    return 0

'''
DFS backtracks, recomputing the number of ways to get from idx I to the end of the string.
Explicitly memoize this, starting from the back.
'''

def nways(opts, pattern, cache, start_idx):
    nwins = 0
    visited = set()
    q = [(0, '')] # Holds amount of pattern consumed, hash of opts to get there
    mypattern = pattern[start_idx:]
    while len(q) > 0:
        pat_idx, opt_hash = q.pop()
        global_idx = pat_idx + start_idx
        if global_idx in cache:
            nwins += cache[global_idx]
            continue
        for i, opt in enumerate(opts):
            if mypattern[pat_idx:].startswith(opt):
                upto = pat_idx+len(opt)
                nhash = opt_hash + f'_{i+1}'
                if nhash not in visited:
                    q.append((upto, nhash))
                    visited.add(nhash)
        
    return nwins

def total_nways(opts, puzzle):
    idx_to_nways = {}
    idx_to_nways[len(puzzle)] = 1
    for i in range(0, len(puzzle)):
        start_idx = len(puzzle) - 1 - i
        this_ways = nways(opts, puzzle, idx_to_nways, start_idx)
        idx_to_nways[start_idx] = this_ways
    return idx_to_nways[0]


p1 = sum(map(lambda p: construct(opts, p), patterns))
print(f'part1: {p1}')

p2 = sum(map(lambda p: total_nways(opts, p), patterns))
print(f'part2: {p2}')
