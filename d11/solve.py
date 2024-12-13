# part 1 
# dynamic programming?
# do it the dumb way first, then dynamic programming!
file = 'input.txt'
stones = list(map(int, open(file).read().strip().split()))
res = 0
steps = 25
print('beginning')
print(' '.join(list(map(str, stones))))

def transform(stone):
    if stone == 0:
        return [1]
    stonestr = str(stone)
    stonelen = len(stonestr)
    if stonelen % 2 == 0:
        return [int(stonestr[:stonelen//2]), int(stonestr[stonelen//2:])]
    return [stone * 2024]

for step in range(steps):
    next_stones = []
    for stone in stones:
        next_stones.extend(transform(stone))
    stones = next_stones

print(len(stones))


# part 2
# dynamic programming?
# do it the dumb way first, then dynamic programming!
"""
.plan
This is fractal.
0
1
2024
20            24
2       0     2       4
4048    1     4048    8096
40  48  2024  40  48  80  96
4 0 4 8 20 24 4 0 4 8 8 0 9 6

How long does it take to compute one stone all the way to 75?
I can't even do that, it stalls out in the 40s.

I can memoize each unique number I come across and how many stones it decomposes into after N steps.
This will give a shortcut lookup that builds in usefulness over time

I'm an iterative guy so I'll do it iteratively.
Sike, recursive is a great fit

The difficult part is propagating contributions back up the tree
"""
file = 'input.txt'
stones = list(map(int, open(file).read().strip().split()))
res = 0
n_steps = 75
print('beginning')
print(' '.join(list(map(str, stones))))

from collections import defaultdict
'''
Maps
stone_id -> map(steps -> num_children)
'''
cache = defaultdict(dict)
def transform(stone):
    if stone == 0:
        return [1]
    stonestr = str(stone)
    stonelen = len(stonestr)
    if stonelen % 2 == 0:
        return [int(stonestr[:stonelen//2]), int(stonestr[stonelen//2:])]
    return [stone * 2024]

def descend(stone, n_steps):
    if n_steps == 0:
        return 1
    ret = cache[stone].get(n_steps)
    if ret:
        return ret
    
    # drink full and descend
    children = transform(stone)
    ret = 0
    for child in children:
        ret += descend(child, n_steps-1)

    # How does that affect my count?
    cache[stone][n_steps] = ret
    return ret


ret = 0
for stone in stones:
    ret += descend(stone, n_steps=n_steps)

print(ret)