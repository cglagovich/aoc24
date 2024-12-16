# part 1
'''
Puzzle starts with agent facing East.
90 degree turns cost 1000. going forward costs 1
Find the lowest cost to solve the maze.

Datastructure:
map with indexing

Algorithm:
Recursive DFS
- Add current node to the path
- Clone the path
- Call visit on neighbors of this node with the cloned path
- Return all paths which lead to end of maze

- After getting all paths, postprocess to calculate score

def visit(paths, cur_path, cur_coord):
    cur_path.append(cur_coord)
    if maze[cur_coord] == 'E':
        paths.append(cur_path.copy())
        return
    for ncoord in next_moves(cur_coord):
        # Branch the path for each new move we take
        if ncoord not in cur_path and maze[ncoord] != '#':
            path_clone = cur_path.copy()
            visit(paths, path_clone, ncoord)


Algorithm:
Iterative BFS
valid_paths = []
working_paths = [[cur_coord]]
while len(working_paths) > 0:
    p = working_paths.pop(0)
    c = p[-1]
    if maze[c] == 'E':
        valid_paths.append(working_paths.copy())
        continue
    for ncoord in next_moves(cur_coord):
        if ncoord not in p and maze[ncoord] != '#':
            pclone = p.copy()
            pclone.append(ncoord)
            working_paths.append(pclone)             
'''

class Maze:
    def __init__(self, m):
        self.m =  [mm.strip() for mm in m]
        self.R = len(self.m)
        self.C = len(self.m[0])
        
    def __getitem__(self, coord):
        r, c = coord
        if r < 0 and r >= self.R or c < 0 and c >= self.C:
            # Represent OOB as #
            return '#'
        return self.m[r][c]

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.m])

    def get_agent_pos(self):
        for r in range(self.R):
            for c in range(self.C):
                if self[r,c] == 'S':
                    return (r, c)
        assert False

    def next_moves(self, coord):
        '''
        Return next moves which don't lead to '#'
        '''
        ret = []
        for delta in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nc = coord[0] + delta[0], coord[1] + delta[1]
            if self[nc] != '#':
                ret.append(nc)
        return ret

def visit_dfs(maze, paths, cur_path, cur_coord):
    cur_path.append(cur_coord)
    if maze[cur_coord] == 'E':
        paths.append(cur_path.copy())
        return
    for ncoord in maze.next_moves(cur_coord):
        # Branch the path for each new move we take
        if ncoord not in cur_path and maze[ncoord] != '#':
            path_clone = cur_path.copy()
            visit_dfs(maze, paths, path_clone, ncoord)

def score(path):
    direc_to_delta = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}
    delta_to_direc = {v: k for k, v in direc_to_delta.items()}
    def turn(direc, c0, c1):
        # Returns new direc and how many turns it takes to get there
        delta = c1[0] - c0[0], c1[1] - c0[1]
        direc_delta = direc_to_delta[direc]
        new_direc = delta_to_direc[delta]
        if delta == direc_delta:
            return new_direc, 0
        if sum(map(lambda x: x[0] * x[1], zip(delta, direc_delta))) == 0:
            # orthogonal, so 90 degree turn
            return new_direc, 1
        
        # 180 degree turn (should never be done!)
        assert False
        assert direc[0] == -direc_delta[0] and direc[1] == -direc_delta[1]
        return 2
    
    score = 0
    direc = 'E'
    for idx in range(1, len(path)):
        prev_coord = path[idx-1]
        coord = path[idx]
        direc, n_turns = turn(direc, prev_coord, coord)
        score += 1 + n_turns * 1000
    return score

fname = 'sample.txt'
maze = Maze(open(fname).readlines())
print(maze)

agent_pos = maze.get_agent_pos()
print(f'{agent_pos=}')

# Use dfs
# paths = []
# cur_path = []
# visit_dfs(maze, paths, cur_path, agent_pos)

# Use bfs
paths = []
working_paths = [[agent_pos]]
while len(working_paths) > 0:
    # print(f'{len(working_paths)=}')
    p = working_paths.pop(0)
    # print(f'{p=}')
    c = p[-1]
    # print(f'{c=}')
    if maze[c] == 'E':
        paths.append(p.copy())
        continue
    for ncoord in maze.next_moves(c):
        if ncoord not in p and maze[ncoord] != '#':
            # print(f'{ncoord=}')
            pclone = p.copy()
            pclone.append(ncoord)
            working_paths.append(pclone)

min_score = float('inf')
for idx, p in enumerate(paths):
    print(f'path {idx}')
    # print(p)
    path_score = score(p)
    min_score = min(min_score, path_score)
    print(f'score: {score(p)}')
    assert maze[p[-1]] == 'E'
    for coord in p:
        assert maze[coord] != '#'

print(min_score)



