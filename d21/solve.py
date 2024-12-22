numpad = {
    '7':        complex(0, 0),
    '8':        complex(0, 1),
    '9':        complex(0, 2),
    '4':        complex(1, 0),
    '5':        complex(1, 1),
    '6':        complex(1, 2),
    '1':        complex(2, 0),
    '2':        complex(2, 1),
    '3':        complex(2, 2),
    'illegal':  complex(3, 0),
    '0':        complex(3, 1),
    'A':        complex(3, 2),
}

dirpad = {
    'illegal':  complex(0, 0),
    '^':        complex(0, 1),
    'A':        complex(0, 2),
    '<':        complex(1, 0),
    'v':        complex(1, 1),
    '>':        complex(1, 2),
}

delta_to_dir = {
    complex(1, 0):  'v',
    complex(-1, 0): '^',
    complex(0, 1):  '>',
    complex(0, -1): '<',
    complex(0, 0): '',
}

dir_to_delta = {v: k for k, v in delta_to_dir.items()}

def direc_commands(start, end):
    '''
    Given start and end pos, return a sequence of directional
    chars which gets you there.
    '''
    delta = end - start
    rdelta = complex(delta.real, 0)
    rcommands = ""
    if rdelta != 0:
        runit = rdelta / abs(rdelta)
        rcommands = delta_to_dir[runit] * int(abs(rdelta))

    cdelta = complex(0, delta.imag)
    ccommands = ""
    if cdelta != 0:
        cunit = cdelta / abs(cdelta)
        ccommands = delta_to_dir[cunit] * int(abs(cdelta))

    return rcommands + ccommands

def is_legal_command(seq, pad, start_id='A'):
    '''
    Determine if this command would put a robot finger over the empty space
    '''
    avoid = pad['illegal']
    curpos = pad[start_id]
    for ch in seq:
        if ch == 'A':
            continue
        curpos = curpos + dir_to_delta[ch]
        if curpos == avoid:
            return False
    return True

from itertools import permutations
from functools import cache

@cache
def minsolve(code, depth, maxdepth):
    '''
    Given a code and a depth, return the sum of all smallest length top-level programs
    which produces that code.

    How it works:
    Iterate over all chars in this code
    For each char, find a sequence of commands at the next lower level which generates that char
    Create a set of all valid permutations of that sequence of commands
    Get the minimum length top-level-command by calling minsolve one layer deeper on each permuation

    Sum all minimum length top-level-commands to generate each char in this sequence
    Return that
    '''
    pad = numpad if depth == 0 else dirpad
    if depth == maxdepth:
        return len(code) 
    start_id = 'A'
    start_pos = pad[start_id]
    codelen = 0
    for ch in code:
        nextpos = pad[ch]
        # This is one possible set of buttons to push to get the current cursor over `ch`
        cardinals = direc_commands(start_pos, nextpos)
        cardinal_perms = set(''.join(perm) for perm in permutations(cardinals))
        cardinal_perms = filter(lambda x: is_legal_command(x, pad, start_id=start_id), cardinal_perms)
        ch_min_len = min(minsolve(perm+'A', depth+1, maxdepth) for perm in cardinal_perms)
        codelen += ch_min_len
        start_pos = nextpos
        start_id = ch
    return codelen

def code_complexity(code, maxdepth):
    minlen = minsolve(code, 0, maxdepth)
    codenum = int(code.split('A')[0])
    return codenum * minlen

def solve(codes, maxdepth):
    return sum(map(lambda code: code_complexity(code, maxdepth), codes))

import sys
fname = sys.argv[1]
codes = [c.strip() for c in open(fname).readlines()]

# part 1
print('part 1:', solve(codes, 3))

# part 2
print('part 2:', solve(codes, 26))
