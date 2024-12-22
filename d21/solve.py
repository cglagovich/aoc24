'''
This has three levels of remotes.
1. Human pressed directional
2. Robot pressed direciontal
3. Robot pressed directional
4. Robot pressed numeric

Result: arithmetic expressions which requires the shortest sequence of commands
the human will press in order to get the code entered.
Notes: 
- greedily finding the shortest sequence of commands from bottom up may not be optimal,
but at first I will pretend that it is.
- robot arms must avoid the empty space on each pad

This is one problem but wrapped up three times.
Solution:
- given a sequence, a target pad, and a source pad, output the minimal set of commands to achieve that sequence
- apply this function on the three pads

Greedy does not give the right answer. It is possible that one sequence of <<<^^
on a keypad leads to more button presses on the higher level than <^<^<. 

Here's a dumb idea: 
- For each level of directional commands except for the last, brute force produce
all variations of orderings for sequences between 'A' commands. Take each of these
permutations all the way to the top, picking the one with the smallest length.
- I implemented this and it sort of works, but I get a lower result than expected. 
I think that's because I'm creating invalid paths that go over the illegal space.
I need to filter by legal commands.
- My answer was too high again. I think another problem I had was that I'm not generating all permutations.
For each permutation of the first run, I'm not enumerating all permutation of the next run and so forth.

^ Turns out that this worked! However, it takes 31.88 seconds to run.
For Part 2 it might take...... forever.
There must be some structure to the problem that I don't understand. Maybe, given a chain of robots,
there's some always optimal way to get to a specific part of the keypad. 
I see the example usually has `<v<` rather than `v<<` or `<<v`.
Or maybe there's a way to solve this with dynamic programming.

Potential, fast iterative solution.
Do this command by command, breaking down the problem. 
For each `start -> end` pair of positions on a specific pad, there is at least one optimal path
    which results in the fewest commands at the highest level.
I think I have to do this both recursively and iteratively.
- For each command, recurse all the way to the top to find the shortest top level command to get there
- Keep track of starting position for each command


def min_len_of_command(pads_left=0, )

Maybe less dumb idea:
- For each possible start and end delta at each level, brute force all possible
ways of getting there at the level and all upper levels. This builds a cache
for each level and can find the smallest path at the top level for any input.



+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+


    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+


<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
v<<A>>^A<A>AvA<^AA>A<vAAA>^A
<A^A>^^AvvvA
029A
'''

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

def direc_commands(start, end, avoid):
    '''
    For any path, we have two options. Do R then C, or C then R
    If start is in the same row as avoid, do R.
    If start is in the same col as avoid, do C.
    Otherwise, do R.
    '''
    first_dir = 'real' if start.real == avoid.real else 'imag'

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

    commands = rcommands + ccommands if first_dir == 'real' else ccommands + rcommands

    return commands

def is_legal_command(seq, pad, start_id='A'):
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
from functools import lru_cache


'''
Recursive solving function
Given a code, startpos, and depth, it returns the min length of the topmost program to produce that code.

It iterates over the characters of a code.
For each character,
    return the minimum length of all solutions
return the sum of character lengths

Is it the case that anyone who enters this function is starting on 'A'?
At the beginning, every single robot is on A
Every command ends in A, so every start pos is 'A'
'''

@lru_cache
def minsolve(code, depth, maxdepth):
    pad = numpad if depth == 0 else dirpad
    if depth == maxdepth:
        return len(code) 
    start_id = 'A'
    start_pos = pad[start_id]
    codelen = 0
    for ch in code:
        nextpos = pad[ch]
        # This is one possible set of buttons to push to get the current cursor over `ch`
        buttons = direc_commands(start_pos, nextpos, pad['illegal'])
        allbuttons = filter(lambda x: is_legal_command(x, pad, start_id=start_id), set(''.join(perm) for perm in permutations(buttons)))
        ch_min_len = min(minsolve(button+'A', depth+1, maxdepth) for button in allbuttons)
        codelen += ch_min_len
        start_pos = nextpos
        start_id = ch
    return codelen

def code_complexity(code, maxdepth):
    minlen = minsolve(code, 0, maxdepth)
    codenum = int(code.split('A')[0])
    res = codenum * minlen
    return res

def solve(codes, maxdepth):
    res = 0
    for code in codes:
        res += code_complexity(code, maxdepth)
    return res



import sys
fname = sys.argv[1]
codes = [c.strip() for c in open(fname).readlines()]

# part 1
print('part 1:', solve(codes, 3))

# part 2
print('part 2:', solve(codes, 26))
