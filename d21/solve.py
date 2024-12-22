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

def is_legal_command(seq, pad):
    avoid = pad['illegal']
    curpos = pad['A']
    for ch in seq:
        if ch == 'A':
            continue
        curpos = curpos + dir_to_delta[ch]
        if curpos == avoid:
            return False
        
    return True


def command_sequence(seq, pad):
    '''
    Given a target sequence and a target pad, 
    determine the commands required to input that sequence into the pad.
    '''
    commands = ""
    curpos = pad['A']
    for ch in seq:
        # print(f'char {ch} is at {pad[ch]}')
        nextpos = pad[ch]
        curcommands = direc_commands(curpos, nextpos, pad['illegal'])
        curcommands += 'A'
        commands += curcommands
        # print(''.join(curcommands))
        curpos = nextpos
    return commands

from itertools import permutations

def all_permutations(seq):
    '''
    Buggy because it doesn't generate all permutations
    '''
    splits = seq.split('A')
    for idx, split in enumerate(splits[:-1]):
        for perm in permutations(split):
            yield 'A'.join(splits[:idx] + [''.join(perm)] + splits[idx+1:])

def all_permutations_rec(seq):
    '''
    Naturally recursive. For each permutation of the first run, yield it with all permutations of the next run
    '''
    splits = seq.split('A')
    split = splits[0]
    perms = set(permutations(split))
    if len(splits) == 2:
        for perm in perms:
            yield ''.join(perm) + 'A'
    else:
        for perm in perms:
            for nextperm in all_permutations_rec('A'.join(splits[1:])):
                yield ''.join(perm) + 'A' + nextperm


def solve(code):
    '''
    Few stages to this
    '''
    commands = [[code]]

    print(f'solving {code}')
    for idx, pad in enumerate([numpad, dirpad, dirpad]):
        min_len = float('inf')
        print(f'\tpad {idx}')
        targets = commands[-1]
        cur_acc = []
        for t in targets:
            base_command = command_sequence(t, pad)
            if len(base_command) <= min_len:
                min_len = len(base_command)
            else:
                continue
            print(f'\t\ttarget {t}')
            # print(f'base_command: {base_command}')
            permutations = set(all_permutations_rec(base_command))
            # for perm in permutations:
            #     print(perm)
            permutations = filter(lambda x: is_legal_command(x, pad), permutations)
            cur_acc.extend(list(permutations))
            print(f'\t\tcur_acc len {len(cur_acc)}')
            # commands.append(list(permutations))
        # remove all cur commands longer than longest cur command
        min_len = min(len(c) for c in cur_acc)
        cur_acc = list(filter(lambda x: len(x) == min_len, cur_acc))
        commands.append(cur_acc)


    # print(f'{len(commands)=}')
    # print(f'{len(commands[-1])=}')
    # breakpoint()
    # print('\n'.join(reversed(commands)))
    smallest = sorted(commands[-1], key=lambda x: len(x))[0]
    # print(smallest, len(smallest))
    codenum = int(code.split('A')[0])
    res = codenum * len(smallest)
    print(f'{codenum} * {len(smallest)} = {res}')
    return res


# allperms = '\n'.join(sorted(list(set(all_permutations_rec('<^^^AvvvA^^A>vvA')))))
# print(allperms)
# breakpoint()

import sys
fname = sys.argv[1]
codes = open(fname).readlines()

# part 1
ret = 0
for code in codes:
    code = code.strip()
    ret += solve(code)
print('part 1:', ret)