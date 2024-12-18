# part 1
import heapq
import sys
n_bytes = int(sys.argv[2])
grid_dim = int(sys.argv[3])
print(f'n_bytes: {n_bytes}, grid dim: {grid_dim}')
fname = sys.argv[1]
inp = list(map(lambda line: tuple(map(lambda x: int(x), [l for l in line.strip().split(',')])), open(fname).readlines()))

start_pos = 0 + 0j # r + c*j
dirs = [1+0j, -1+0j, 0+1j, 0-1j]

def search(walls):
    visited = set()
    visited.add(start_pos)
    pq = []
    heapq.heappush(pq, (0, start_pos.real, start_pos.imag))
    nsteps = 0
    while len(pq) > 0:
        nsteps += 1
        cost, *cur_pos = heapq.heappop(pq)
        cur_pos = complex(*cur_pos)
        if cur_pos == complex(grid_dim, grid_dim):
            return cost
        for ndir in dirs:
            npos = cur_pos + ndir
            if npos.real < 0 or npos.real > grid_dim or npos.imag < 0 or npos.imag > grid_dim:
                continue
            if npos not in visited and (npos.real, npos.imag) not in walls:
                heapq.heappush(pq, (cost+1, npos.real, npos.imag))
                # Greedy?
                visited.add(npos)
    return False

# part 1
print('part1', search(inp[:n_bytes]))

# part 2
# Do a binary search to find which byte closes the path
import math
low = n_bytes
high = len(open(fname).readlines())
while low < high - 1:
    mid = (low + high) // 2
    if search(inp[:mid]):
        low = mid
    else:
        high = mid

print(f'part2', inp[low])