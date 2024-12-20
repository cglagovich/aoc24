import sys
fname = sys.argv[1]
min_saved = int(sys.argv[2])
maze = [line.strip() for line in open(fname).readlines()]
length = sum(1 if item == '.' else 0 for line in maze for item in line) + 1
valid_nodes = set(complex(r, c) for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] in "S.E")

'''
Construct a tree. Head is start, tail is end. Each node refers to the next node in the path.
In addition, each node has a cheat, which is the next valid node that it would go to if it cheated.
Note that each node can have multiple cheats.

Then for each node check the length of the path from it to its cheat, and that's the amount of time
saved for that cheat.
'''

class Path:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.cheat_vals = []

    def append(self, next_val):
        next_node = Path(next_val)
        self.next = next_node
        return next_node
    
    def tolist(self):
        p = [self.val]
        cur = self
        while cur.next is not None:
            p.append(cur.next.val)
            cur = cur.next
        return p
    
    def __repr__(self):
        return '->'.join([str(pp) for pp in self.tolist()])
    
    def repr_with_cheats(self):
        p = [(self.val, self.cheat_vals)]
        cur = self
        while cur.next is not None:
            p.append((cur.next.val, cur.next.cheat_vals))
            cur = cur.next
        return '\n'.join(f'{val} : {cheat_val}' for val, cheat_val in p)
    
    def len_to_val(self, val):
        lento = 0
        cur = self
        while cur.next is not None and cur.val != val:
            lento += 1
            cur = cur.next
        return lento
    
    def generate_dists(self):
        cache = {}
        ll = self.tolist()
        for idx, val in enumerate(ll):
            cache[val] = len(ll) - idx
        return cache

def get_manhattan_block(cur, max_l1_dist):
    '''
    Eample, max_l1_dist = 4

    #############
    ######.######
    #####...#####
    ####.....####
    ###.......###
    ##....X....##
    ###.......###
    ####.....####
    #####...#####
    ######.######
    #############
    '''
    # neighbors = []
    for r in range(-max_l1_dist, max_l1_dist+1):
        leftover = max_l1_dist - abs(r)
        for c in range(-leftover, leftover + 1):
            if not (r == 0 and c == 0):
                # neighbors.append(cur + complex(r, c))
                yield cur + complex(r, c)
    # return neighbors


def construct_path(maze, max_l1_dist):
    get_pos_of = lambda goal: [complex(r, c) for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] == goal][0]
    start_pos = get_pos_of('S')
    end_pos = get_pos_of('E')

    filter_neighbors = lambda neighbors: filter(lambda x: x in valid_nodes and x not in visited, neighbors)
    one_away = list(get_manhattan_block(complex(0, 0), 1))
    dist_away = list(get_manhattan_block(complex(0, 0), max_l1_dist))

    head = Path(start_pos)
    visited = set()
    cur = head
    while cur.val != end_pos:
        visited.add(cur.val)
        # First, find the next node in the true path
        # neighbors = get_manhattan_block(cur.val, 1)
        neighbors = map(lambda x: x + cur.val, one_away)
        neighbors = list(filter_neighbors(neighbors))
        assert len(neighbors) == 1
        nnode = cur.append(neighbors[0])

        # Then, get all possible cheats
        # cheats = get_manhattan_block(cur.val, max_l1_dist)
        cheats = map(lambda x: x + cur.val, dist_away)
        cheats = filter_neighbors(cheats)
        cur.cheat_vals = list(cheats)

        cur = nnode
    return head

def get_cheats(head):
    # mapping from node val to dist from end of list, significantly speeds up path len calculation.
    dist_cache = head.generate_dists()
    # For each node, for each cheat, calculate how much time it saves
    l1_dist = lambda x, y: abs(x.real - y.real) + abs(x.imag - y.imag)
    cheat_savings = []
    cur = head
    while cur.next is not None:
        for cv in cur.cheat_vals:
            # Savings is len of uncheated path - length of cheat
            cheat_path_len = dist_cache[cur.val] - dist_cache[cv]
            cheat_len = cheat_path_len - l1_dist(cur.val, cv)
            cheat_savings.append((cheat_len, cur.val, cv))
        cur = cur.next
    return cheat_savings

def sum_savings(savings):
    savings = sorted(savings, key=lambda x: x[0], reverse=True)

    from collections import Counter
    count = Counter([s[0] for s in savings])
    # for k, v in sorted(count.items(), key=lambda x: x[0], reverse=True):
    #     print(f'{v} ways to save {k}')

    final_cheats = sum([v for k, v in count.items() if k >= min_saved])
    
    return final_cheats

head = construct_path(maze, 2)
savings = get_cheats(head)
print(f'part 1:', sum_savings(savings))

# part 2
'''
Now, any point that is L1 distance 20 or less from current node is a potential cheat.
I generalized the above cheat construction code to take a maximum L1 distance.
'''
head = construct_path(maze, 20)
savings = get_cheats(head)
print('part 2:', sum_savings(savings))
