import sys
fname = sys.argv[1]
min_saved = int(sys.argv[2])
maze = [line.strip() for line in open(fname).readlines()]
length = sum(1 if item == '.' else 0 for line in maze for item in line) + 1
valid_nodes = set(complex(r, c) for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] in "S.E")

'''
Construct a tree. Head is start, tail is end. Each node refers to the next node in the path.
In addition, each node has a cheat, which is the next valid node that it would go to if it cheated.
Note that each node can have multiple cheats. # TODO: Add multiple cheats.

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


def construct_path(maze):
    R = len(maze)
    C = len(maze[0])
    get_pos_of = lambda goal: [complex(r, c) for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] == goal][0]
    is_in_bounds = lambda val: val.real >= 0 and val.real < R and val.imag >= 0 and val.imag < C
    start_pos = get_pos_of('S')
    end_pos = get_pos_of('E')
    print(f'start_pos={start_pos}')
    # Construct the valid path
    head = Path(start_pos)
    visited = set()
    cur = head
    while cur.val != end_pos:
        visited.add(cur.val)
        for ndir in [1+0j, -1+0j, 0+1j, 0-1j]:
            nval = cur.val + ndir
            if not is_in_bounds(nval):
                continue
            if nval in visited:
                continue
            if nval not in valid_nodes:
                continue
            cur = cur.append(nval)
            break
    print('constructed path')

    # Construct cheating paths
    cur = head
    visited = set()
    while cur.next is not None:
        visited.add(cur.val)
        for ndir in [1+0j, -1+0j, 0+1j, 0-1j]:
            # Skip over a wall
            wall = cur.val + ndir
            skip = wall + ndir
            if is_in_bounds(wall) and maze[int(wall.real)][int(wall.imag)] == '#' and skip in valid_nodes and skip not in visited:
                cur.cheat_vals.append(skip)

        # Look at the next node
        cur = cur.next
    return head

def get_cheats(head):
    cheat_savings = []
    cur = head
    while cur.next is not None:
        for cv in cur.cheat_vals:
            # Subtract 2 because a cheat takes two moves
            cheat_len = cur.len_to_val(cv) - 2
            cheat_savings.append((cheat_len, cur.val, cv))
        cur = cur.next
    return cheat_savings

def repr_savings(savings):
    savings = sorted(savings, key=lambda x: x[0], reverse=True)
    # for s in savings:
    #     print(f'{s[0]} : {s[1]}->{s[2]}')

    from collections import Counter
    count = Counter([s[0] for s in savings])
    # for k, v in sorted(count.items(), key=lambda x: x[0], reverse=True):
    #     print(f'{v} ways to save {k}')

    final_cheats = sum([v for k, v in count.items() if k >= min_saved])
    print(final_cheats)

head = construct_path(maze)
savings = get_cheats(head)
repr_savings(savings)

# part 2
'''
Now, any point that is L1 distance 20 or less from current node is a potential cheat.
I'll generalize the above cheat construction code to take a maximum L1 distance.
'''

