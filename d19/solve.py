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
        visited.add(pat_idx)
        if pat_idx == len(pattern):
            return 1
        for opt in opts:
            if pattern[pat_idx:].startswith(opt):
                upto = pat_idx+len(opt)
                if upto not in visited:
                    q.append(upto)
        
    return 0

def nways(opts, pattern):
    '''
    DFS to find any pattern which works
    '''
    nways = 0
    visited = set()
    q = [(0, 0)] # Holds amount of pattern consumed, hash of opts to get there
    while len(q) > 0:
        pat_idx, opt_hash = q.pop(0)
        if pat_idx == len(pattern):
            nways += 1
        for i, opt in enumerate(opts):
            if pattern[pat_idx:].startswith(opt):
                upto = pat_idx+len(opt)
                nhash = opt_hash * len(opts) + i
                if upto not in visited:
                    q.append((upto, nhash))
                    visited.add((upto, nhash))
        
    return nways

p1 = sum(map(lambda p: construct(opts, p), patterns))
print(p1)

p2 = sum(map(lambda p: nways(opts, p), patterns))
print(p2)

# for pattern in patterns:
#     cando = construct(opts, pattern)
#     if cando:
#         print(f'Can construct {pattern}')
#     else:
#         print(f'Cannot construct {pattern}')
    
