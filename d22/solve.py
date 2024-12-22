NITERS = 2000

def process(prev, cur):
    cur = prev ^ cur
    cur = cur % 16777216
    return cur

def all_secrets(s):
    for _ in range(NITERS):
        s = process(s, s*64)
        s = process(s, s//32)
        s = process(s, s*2048)
        yield s

def solvep1(codes):
    return sum(map(lambda c: list(all_secrets(c))[-1], codes))


def secretmap(s):
    prices = list(map(lambda x: x % 10, [s] + list(all_secrets(s))))

    diffmap = {}
    diffi = lambda i, j: prices[i - j+1] - prices[i - j]
    for i in range(4, len(prices)):
        d0 = diffi(i, 4)
        d1 = diffi(i, 3)
        d2 = diffi(i, 2)
        d3 = diffi(i, 1)
        diff = (d0, d1, d2, d3)
        diffmap.setdefault(diff, prices[i])

    return diffmap

def solvep2(codes):
    diffmaps = []
    for code in codes:
        diffmaps.append(secretmap(code))

    alldiffs = set([k for dm in diffmaps for k in dm.keys()])

    maxrev = 0
    for diff in alldiffs:
        newrev = sum([dm[diff] for dm in diffmaps if diff in dm])
        maxrev = max(maxrev, newrev)

    return maxrev

import sys
fname = sys.argv[1]
codes = [int(c.strip()) for c in open(fname).readlines()]

print('part 1:', solvep1(codes))
print('part 2:', solvep2(codes))