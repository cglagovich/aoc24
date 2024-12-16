# part 1
fname = 'input.txt'
inp = open(fname).read()
m, instrs = inp.split('\n\n')

class Map:
    def __init__(self, m):
        self.m = [[mmm for mmm in mm.strip()] for mm in m.split('\n')]
        self.R = len(self.m)
        self.C = len(self.m[0])

    def __getitem__(self, tup):
        r, c = tup
        assert r >= 0 and r < self.R
        assert c >= 0 and c < self.C
        return self.m[r][c]
    
    def __setitem__(self, tup, value):
        r, c = tup
        self.m[r][c] = value

    def try_move(self, tup, dir):
        # Returns coord tup after attempting to move in a direction
        assert self[tup] == '@'
        # If there is a '.' between the agent and the nearest wall, it can move
        can_move = False
        next_elem = (tup[0] + dir[0], tup[1] + dir[1])
        while True:
            try:
                val = self[next_elem]
                if val == '#':
                    break
                if val == '.':
                    can_move = True
                    break
            except:
                break
            next_elem = (next_elem[0] + dir[0], next_elem[1] + dir[1])
        
        if not can_move:
            return tup
        
        # Now shift boxes iteratively
        next_idx = (tup[0] + dir[0], tup[1] + dir[1])
        replaced = self[next_idx]
        self[next_idx] = '@'
        self[tup] = '.'

        if replaced == 'O':
            while True:
                # Find the first '.' after a string of 'O' and replace it with 'O'
                next_idx = (next_idx[0] + dir[0], next_idx[1] + dir[1])
                if self[next_idx] == '.':
                    self[next_idx] = 'O'
                    break
        return (tup[0] + dir[0], tup[1] + dir[1])

    def print(self):
        print('\n'.join([''.join(row) for row in self.m]))

    def get_agent_pos(self):
        for r in range(self.R):
            for c in range(self.C):
                if self[r,c] == '@':
                    return (r, c)
        assert False

    def calculate_score(self):
        # Calculate score of the map
        score = 0
        for r in range(self.R):
            for c in range(self.C):
                if self[r, c] == 'O':
                    score += 100*r + c
        return score
    
m = Map(m)
# m.print()
instrs = instrs.replace('\n', '')
# print(instrs)

instr_map = {'<': (0, -1), 'v': (1, 0), '>': (0, 1), '^': (-1, 0)}
agent_pos = m.get_agent_pos()
print(f'{agent_pos=}')
for inu, c in enumerate(instrs):
    # print(f'instr[{inu}] {c}')
    delta = instr_map[c]
    agent_pos = m.try_move(agent_pos, delta)
    # m.print()

score = m.calculate_score()
print(score)



# part 2
fname = 'input.txt'
inp = open(fname).read()
m, instrs = inp.split('\n\n')

class Coord:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    def __add__(self, rhs):
        return Coord(self.r + rhs.r, self.c + rhs.c)
    @property
    def tup(self):
        return (self.r, self.c)
    def __repr__(self):
        return f'Coord(r={self.r}, c={self.c})'
    def __hash__(self):
        return hash(self.tup)
    def __eq__(self, rhs):
        return self.r == rhs.r and self.c == rhs.c
class Map:
    def __init__(self, m):
        mapping = {'#': '##', '@': '@.', '.': '..', 'O': '[]'}
        self.m = [[mmmm for mmm in mm.strip() for mmmm in mapping[mmm]] for mm in m.split('\n')]
        self.R = len(self.m)
        self.C = len(self.m[0])
        
    def __getitem__(self, tup):
        r, c = tup
        assert r >= 0 and r < self.R
        assert c >= 0 and c < self.C
        return self.m[r][c]
    
    def __setitem__(self, tup, value):
        r, c = tup
        self.m[r][c] = value

    def updown_move(self, tup, dir):
        '''
        Handle up/down moves which are more complicated
        '''
        '''
        Recursively search the tree of boxes that WOULD move if we moved.
        '''
        cur_coord = Coord(*tup)
        dir = Coord(*dir)
        def can_move_updown(tup, dir):
            next_coord = tup + dir
            try:
                next_val = self[next_coord.tup]
                print(f'map[{next_coord.tup}]={next_val}')
                if next_val == '#':
                    return False
                elif next_val == '.':
                    return True
                else:
                    # Iterate over boxes [] and add their nexts to this
                    next_can_move = []
                    next_coords = []
                    assert next_val in '[]'
                    next_coords.append(next_coord)
                    if next_val == '[':
                        next_coords.append(next_coord + Coord(0, 1))
                    else:
                        next_coords.append(next_coord + Coord(0, -1))
                    for nc in next_coords:
                        next_can_move.append(can_move_updown(nc, dir))
                    return all(next_can_move)
            except Exception as e:
                # out of bounds
                print(f'Exception {e}')
                return False
            
        print('Trying updown')
        if not can_move_updown(cur_coord, dir):
            print('Failed')
            return tup
        print('Passed')

        # Implement the logic to actually move
        other_bracket_delta = {'[': Coord(0, 1), ']': Coord(0, -1)}
        boxes = set()
        def visit(idx, dir):
            next_idx = idx + dir
            try:
                next_val = self[next_idx.tup]
                print(next_idx, next_val)
                if next_val in '[]':
                    other_idx = next_idx + other_bracket_delta[next_val]
                    boxes.add(next_idx)
                    boxes.add(other_idx)
                    visit(next_idx, dir)
                    visit(other_idx, dir)
            except Exception as e:
                print(f'Exception {e}')
                pass
        visit(cur_coord, dir)
        sort_mult = 1 if dir.r == -1 else -1
        boxes = sorted(list(boxes), key=lambda x: x.r * sort_mult)
        # print(boxes)

        for b in boxes:
            # do the shift
            self[(b+dir).tup] = self[b.tup]
            self[b.tup] = '.'
        
        # Now shift the agent
        self[(cur_coord + dir).tup] = '@'
        self[cur_coord.tup] = '.'

        return (cur_coord + dir).tup
    
    def side_move(self, tup, dir):
        '''
        Handle simple east-west moves
        '''
        can_move = False
        next_elem = (tup[0] + dir[0], tup[1] + dir[1])
        while True:
            try:
                val = self[next_elem]
                if val == '#':
                    break
                if val == '.':
                    can_move = True
                    break
            except:
                break
            next_elem = (next_elem[0] + dir[0], next_elem[1] + dir[1])
        
        if not can_move:
            return tup
        
        # Now shift boxes iteratively
        next_idx = (tup[0] + dir[0], tup[1] + dir[1])
        replaced = self[next_idx]
        self[next_idx] = '@'
        self[tup] = '.'

        mapping = {'[': ']', ']': '['}
        dir_mapping = {-1: '[', 1: ']'}
        if replaced in '[]':
            while True:
                # Find the first '.' after a string of 'O' and replace it with 'O'
                next_idx = (next_idx[0] + dir[0], next_idx[1] + dir[1])
                if self[next_idx] in mapping:
                    self[next_idx] = mapping[self[next_idx]]
                elif self[next_idx] == '.':
                    self[next_idx] = dir_mapping[dir[1]]
                    break
                else:
                    assert False
        return (tup[0] + dir[0], tup[1] + dir[1])

    def try_move(self, tup, dir):
        # Returns coord tup after attempting to move in a direction
        assert self[tup] == '@'
        if dir[0] != 0:
            return self.updown_move(tup, dir)
        elif dir[1] != 0:
            return self.side_move(tup, dir)
        else:
            assert False
        

    def print(self):
        print('\n'.join([''.join(row) for row in self.m]))

    def get_agent_pos(self):
        for r in range(self.R):
            for c in range(self.C):
                if self[r,c] == '@':
                    return (r, c)
        assert False

    def calculate_score(self):
        # Calculate score of the map
        score = 0
        for r in range(self.R):
            for c in range(self.C):
                if self[r, c] == '[':
                    score += 100*r + c
        return score
    
m = Map(m)
m.print()
instrs = instrs.replace('\n', '')

instr_map = {'<': (0, -1), 'v': (1, 0), '>': (0, 1), '^': (-1, 0)}
agent_pos = m.get_agent_pos()
print(f'{agent_pos=}')
for inu, c in enumerate(instrs):
    # print(f'instr[{inu}] {c}')
    delta = instr_map[c]
    agent_pos = m.try_move(agent_pos, delta)
    # m.print()

score = m.calculate_score()
print(score)
