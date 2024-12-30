def evaluate(inits, gates):
    wires = inits.copy()
    gates = gates.copy()
    miss_count = 0
    while len(gates) != 0:
        g = gates.pop(0)
        (src0, oper, src1, dst) = g
        if src0 in wires and src1 in wires:
            # execute
            wires[dst] = logic_map[oper](wires[src0], wires[src1])
            miss_count = 0
        else:
            # defer
            miss_count += 1
            if miss_count > len(gates):
                # We've already missed this one! Graph is not a DAG
                raise Exception("You can't do that")
            gates.append(g)

    # print('\n'.join([f'{w}: {int(v)}' for w, v in sorted(wires.items(), key=lambda x: x[0])]))

    zwires = ''.join(str(int(v)) for k, v in sorted(wires.items(), key=lambda x: x[0], reverse=True) if k.startswith('z'))
    return zwires

def solvep1(inits, gates):
    zwires = evaluate(inits, gates)
    zval = int(zwires, base=2)
    return zval

import random
test_cases_fast = [(2**j, 2**j) for j in range(45)] + \
    [(2**j, 0) for j in range(45)] + \
    [(0, 2**j) for j in range(45)]# + \
    # [(2**45-1, 0), (0, 2**45-1)]
    # [(2**45-1, 2**45-1)] + \
# test_cases_slow =  [(random.randrange(0, 2**45), random.randrange(0, 2**45)) for _ in range(1000)]

def solvep2(gates):
    '''
    Plan: With some minimal tests, identify output bits (as a result of carry or sum) which 
    are always incorrect. The switched outputs must be downstream of these bad output bits.
    Find all downstream gates and try all pairs of gates
    '''
    BITLEN = 45
    def rand_init(s, randnum=None):
        if randnum is None:
            randnum = random.randrange(0, 2**BITLEN)
        randstr = '{0:045b}'.format(randnum)
        # randstr = f'{randstr:045d}'
        randbools = reversed([bool(int(val)) for val in randstr])
        rand = {f'{s}{idx:02d}': val for idx, val in enumerate(randbools)}
        return randnum, randstr, rand
    
    def mismatch_idxs(exp, got):
        res = set()
        for idx, (a, b) in enumerate(zip(exp, got)):
            if a != b:
                res.add(len(exp) - 1 - idx)
        return res
    
    def get_bad_positions(gates):
        bad_output_positions = set()

        # Find positions which have bad outputs
        # test_cases_fast = [(2**5-1, 2**5-1)]
        # test_cases_fast = [(i, j) for i in range(2**5) for j in range(2**5)]
        for (xcase, ycase) in test_cases_fast:
            xnum, xbin, xrand = rand_init('x', xcase)
            ynum, ybin, yrand = rand_init('y', ycase)
            xrand.update(yrand)
            inits = xrand
            expect_str = f'{xnum+ynum:046b}'
            # TODO: Remove this debug statement
            # print('WARNING: Doing this for AND test case')
            # expect_str = f'{xnum&ynum:06b}'

            # print(inits)
            # breakpoint()
            zwires = evaluate(inits, gates)
            if zwires != expect_str:
                # print(f'{xnum} + {ynum} = {xnum + ynum}')
                # print(f'x = \t 0b{xbin}')
                # print(f'y = \t 0b{ybin}')
                # print(f'sum = \t0b{expect_str}')
                # print(f'got = \t0b{zwires}')
                # print('WRONG')
                bad_output_positions |= mismatch_idxs(expect_str, zwires)
        return bad_output_positions

    bad_output_positions = get_bad_positions(gates)
    print(f'bad output idxs: {bad_output_positions}')

    # Blacklist certain gates which propagate the correct result upward
    def get_sus_gates(gates, bad_positions):
        def descend(gates, gate, res):
            res.add(gate)
            src0, _, src1, _ = gate
            for g in gates:
                _, _, _, dst = g
                if dst in [src0, src1]:
                    descend(gates, g, res)
        sus = set()
        for bp in bad_positions:
            res = set()
            endgate = list(filter(lambda x: x[3] == f'z{bp:02d}', gates))[0]
            descend(gates, endgate, res)
            sus |= res
        return sus
    
    sus = get_sus_gates(gates, bad_output_positions)
    print(f'sus: {sus}')
    print(f'{len(sus)=}')

    '''
    Now we have the sus gates. Do a brute force over them.
    For each pair of gates, add that pair to the swap list if it reduces the number of bad output idxs. 
    '''
    checked_swaps = []
    sus = list(sus)
    for i in range(len(sus)):
        print('i',i)
        for j in range(i+1, len(sus)):
            # print('j',j)
            new_gates = gates.copy()
            sus0 = gates[i]
            sus1 = gates[j]
            sus0prime = (sus0[0], sus0[1], sus0[2], sus1[3])
            sus1prime = (sus1[0], sus1[1], sus1[2], sus0[3])
            new_gates[i] = sus0prime
            new_gates[j] = sus1prime
            try:
                new_bads = get_bad_positions(new_gates)
                if len(new_bads) < len(bad_output_positions):
                    checked_swaps.append(sus0)
                    checked_swaps.append(sus1)
                    print(f'got a better one, with {new_bads}')
                    break
            except Exception as e:
                # print(e)
                pass

    print('swaps:')
    print(checked_swaps)


            




import sys
fname = sys.argv[1]
inits, gatesinp = open(fname).read().split('\n\n')
inits = {k[0]: bool(int(k[1])) for line in inits.split('\n') if (k:= line.split(':'))}
# print(inits)
gatesinp = sorted(gatesinp.split('\n'))
# print('\n'.join(gatesinp))

logic_map = {
    'XOR': lambda a, b: a ^ b, 
    'OR': lambda a, b: a or b,
    'AND': lambda a, b: a and b,
}

gates = []
for g in gatesinp:
    expr, dst = g.split('->')
    src0, oper, src1 = expr.strip().split(' ')
    src0, src1 = sorted([src0, src1])
    dst = dst.strip()
    gates.append((src0, oper, src1, dst))

# print('\n'.join(' '.join(g) for g in sorted(gates)))

print('part 1: ', solvep1(inits, gates))

print('part 2: ', solvep2(gates))