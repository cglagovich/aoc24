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
m.print()
instrs = instrs.replace('\n', '')
print(instrs)

instr_map = {'<': (0, -1), 'v': (1, 0), '>': (0, 1), '^': (-1, 0)}
agent_pos = m.get_agent_pos()
print(f'{agent_pos=}')
for inu, c in enumerate(instrs):
    print(f'instr[{inu}] {c}')
    delta = instr_map[c]
    agent_pos = m.try_move(agent_pos, delta)
    # m.print()

score = m.calculate_score()
print(score)



# part 2
fname = 'sample.txt'
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
m.print()
instrs = instrs.replace('\n', '')
print(instrs)

instr_map = {'<': (0, -1), 'v': (1, 0), '>': (0, 1), '^': (-1, 0)}
agent_pos = m.get_agent_pos()
print(f'{agent_pos=}')
for inu, c in enumerate(instrs):
    print(f'instr[{inu}] {c}')
    delta = instr_map[c]
    agent_pos = m.try_move(agent_pos, delta)
    # m.print()

score = m.calculate_score()
print(score)
