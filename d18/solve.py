import sys
n_bytes = int(sys.argv[2])
grid_dim = int(sys.argv[3])
print(f'n_bytes: {n_bytes}, grid dim: {grid_dim}')
fname = sys.argv[1]
inp = list(map(lambda line: tuple(map(lambda x: int(x), [l for l in line.strip().split(',')])), open(fname).readlines()))

start_pos = 0 + 0j # r + c*j
dirs = [1+0j, -1+0j, 0+1j, 0-1j]
end_pos = complex(grid_dim, grid_dim)

def search(walls):
    visited = set(walls)
    visited.add((start_pos.real, start_pos.imag))
    q = [(0, start_pos)]
    while len(q) > 0:
        cost, cur_pos = q.pop(0)
        if cur_pos == end_pos:
            return cost
        for ndir in dirs:
            npos = cur_pos + ndir
            nposr, nposi = npos.real, npos.imag
            if nposr < 0 or nposr > grid_dim or nposi < 0 or nposi > grid_dim:
                continue
            if (nposr, nposi) not in visited:
                q.append((cost+1, npos))
                # Greedy?
                visited.add((nposr, nposi))
    return False

# part 1
print('part1', search(inp[:n_bytes]))

# part 2
# Do a binary search to find which byte closes the path
# import math
low = n_bytes
high = len(open(fname).readlines())
while low < high - 1:
    mid = (low + high) // 2
    if search(inp[:mid]):
        low = mid
    else:
        high = mid

print(f'part2', inp[low])