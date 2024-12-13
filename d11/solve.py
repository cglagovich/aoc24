# part 1 

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

"""
.plan

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
Sike, recursive is a great fit.
"""

from collections import defaultdict
'''
Maps
stone_id -> map(steps -> num_children)
'''
cache = defaultdict(dict)
def transform(s):
    return [1] if s == 0 else [int(ss[:len(ss)//2]), int(ss[len(ss)//2:])] if len(ss := str(s)) % 2 == 0 else [s * 2024]

def descend(s, n_steps):
    return 1 if n_steps == 0 else cache[s].get(n_steps) or cache[s].setdefault(n_steps, sum(map(lambda c: descend(c, n_steps=n_steps-1), transform(s))))

print(sum(map(lambda stone: descend(stone, n_steps=75), list(map(int, open('input.txt').read().strip().split())))))
