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
    
    def path_str(self, path):
        grid = [['.' for _ in range(self.C)] for _ in range(self.R)]
        for r in range(self.R):
            for c in range(self.C):
                grid[r][c] = self[r, c]
        for r, c in path:
            grid[r][c] = 'x'
        return '\n'.join([''.join(row) for row in grid])

def visit_dfs(maze, paths, cur_path, cur_coord):
    cur_path.append(cur_coord)
    if maze[cur_coord] == 'E':
        paths.append(cur_path.copy())
        print(f'Found path with score {score(paths[-1])}')
        return
    for ncoord in maze.next_moves(cur_coord):
        # Branch the path for each new move we take
        if ncoord not in cur_path and maze[ncoord] != '#':
            path_clone = cur_path.copy()
            visit_dfs(maze, paths, path_clone, ncoord)

def score(path, direc='E'):
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
        # assert False
        # print(new_direc)
        # print(direc)
        assert delta[0] == -direc_delta[0] and delta[1] == -direc_delta[1]
        return new_direc, 2
    
    score = 0
    for idx in range(1, len(path)):
        prev_coord = path[idx-1]
        coord = path[idx]
        direc, n_turns = turn(direc, prev_coord, coord)
        score += 1 + n_turns * 1000
    return score, direc

fname = 'input.txt'
maze = Maze(open(fname).readlines())
print(maze)

agent_pos = maze.get_agent_pos()
print(f'{agent_pos=}')

# Use dfs
# import sys
# sys.setrecursionlimit(100000)
# paths = []
# cur_path = []
# visit_dfs(maze, paths, cur_path, agent_pos)

# # Use bfs
# paths = []
# working_paths = [[agent_pos]]
# while len(working_paths) > 0:
#     # print(f'{len(working_paths)=}')
#     p = working_paths.pop()
#     c = p[-1]
#     if maze[c] == 'E':
#         paths.append(p)
#         print(f'found a path with score {score(paths[-1])}')
#         continue
#     for ncoord in maze.next_moves(c):
#         if ncoord not in p:
#             pclone = p.copy()
#             pclone.append(ncoord)
#             working_paths.append(pclone)


# # Use tree-based bfs
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.prev = None

# def append(tail, new_val):
#     new_node = Node(new_val)
#     new_node.prev = tail
#     return new_node

# def tail_to_list(tail):
#     cur = tail
#     ret = [cur.val]
#     while cur.prev is not None:
#         cur = cur.prev
#         ret.append(cur.val)
#     return list(reversed(ret))

# def is_in(tail, val):
#     if val == tail.val:
#         return True
#     while tail.prev is not None:
#         tail = tail.prev
#         if val == tail.val:
#             return True
#     return False

# for _ in range(1000):
#     paths = []
#     working_paths = [Node(agent_pos)]
#     # idx = 0
#     while len(working_paths) > 0:
#         # print(f'{len(working_paths)=}')
#         cur_node = working_paths.pop()
#         # if idx % 100000 == 0:
#         #     print(f'{len(working_paths)=}')
#         #     print(f'current node length: {len(tail_to_list(cur_node))}')
#         cur_coord = cur_node.val
#         if maze[cur_coord] == 'E':
#             paths.append(tail_to_list(cur_node))
#             # print(f'found a path with score {score(paths[-1])}')
#             continue
#         for ncoord in maze.next_moves(cur_coord):
#             # TODO: Optimize set lookup
#             # if ncoord not in tail_to_list(cur_node):
#             if not is_in(cur_node, ncoord):
#                 next_node = append(cur_node, ncoord)
#                 working_paths.append(next_node)
#         # idx += 1


import heapq
# # heapq.heappush(pq, (key, data))
# # heapq.heappop(pq)
# # Do Dijkstra
pq = []
heapq.heappush(pq, (0, agent_pos, 'E'))

visited = set()
while len(pq) > 0:
    cost, coord, direc = heapq.heappop(pq)
    visited.add((coord, direc))
    if maze[coord] == 'E':
        print(cost)
        continue
    for ncoord in maze.next_moves(coord):
        ncost, ndirec = score([coord, ncoord], direc)
        if (ncoord, ndirec) not in visited:
            # ncost, ndirec = score([coord, ncoord], direc)
            heapq.heappush(pq, (cost + ncost, ncoord, ndirec))
            # pclone.append(ncoord)
            # working_paths.append(pclone)
    
# print(cost)

# min_score = float('inf')
# for idx, p in enumerate(paths):
#     print(f'path {idx}')
#     path_score, _ = score(p)
#     if path_score < min_score:
#         min_score = path_score
#     print(f'score: {score(p)}')
#     assert maze[p[-1]] == 'E'
#     for coord in p:
#         assert maze[coord] != '#'

# print(min_score)



