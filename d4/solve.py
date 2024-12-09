# part 1

lines = open("input.txt").readlines()

R = len(lines)
C = len(lines[0].strip())

count = 0
for r in range(R):
    for c in range(C):
        if lines[r][c] == 'X':
            m_coords = [((r+i), (c+j)) for i in range(-1, 2) for j in range(-1, 2) if (r+i) < R and (r+i) >= 0 and (c+j) < C and (c+j) >= 0]
            for (mr, mc) in m_coords:
                if lines[mr][mc] == 'M':
                    # Partial match, find the rest
                    dir_r, dir_c = mr - r, mc - c
                    a_coord = (mr + dir_r, mc + dir_c)
                    s_coord = (a_coord[0] + dir_r, a_coord[1] + dir_c)
                    if s_coord[0] in range(0, R) and s_coord[1] in range(0, C):
                        if lines[a_coord[0]][a_coord[1]] == 'A' and lines[s_coord[0]][s_coord[1]] == 'S':
                            count += 1

print(count)

# part 2
save = set()
xcount = 0
MAS = []
for r in range(R):
    for c in range(C):
        if lines[r][c] == 'A':
            m_coords = [((r+i), (c+j)) for i in [-1, 1] for j in [-1, 1] if (r+i) < R and (r+i) >= 0 and (c+j) < C and (c+j) >= 0]
            mas_count = 0
            points = dict()
            completion_dirs = []
            for (mr, mc) in m_coords:
                if lines[mr][mc] == 'M':
                    # Check opposite for A coord
                    dir_r, dir_c = mr - r, mc - c
                    sr, sc = r - dir_r, c - dir_c
                    if not (sr in range(0, R) and sc in range(0, C)):
                        continue
                    if lines[sr][sc] == 'S':
                        mas_count += 1
                        points[(dir_r, dir_c)] = [(r, c), (mr, mc), (sr, sc)]
                        completion_dirs.append((dir_r, dir_c))
                        # print(f'({r},{c}) ({mr},{mc}) ({sr},{sc})')
            if mas_count >= 2:
                orthogonal = False
                for i in range(len(completion_dirs)):
                    for j in range(1, len(completion_dirs)):
                        if sum(map(lambda a: a[0] * a[1], zip(completion_dirs[i], completion_dirs[j]))) == 0:
                            orthogonal = True
                            save |= set(points[completion_dirs[i]])
                            save |= set(points[completion_dirs[j]])
                print(f'A at {r},{c}')
                if orthogonal:
                    xcount += 1

grid = [['.' for _ in range(C)] for _ in range(R)]
for point in save:
    grid[point[0]][point[1]] = lines[point[0]][point[1]]

print('\n'.join(''.join(r) for r in grid))
print(xcount)
