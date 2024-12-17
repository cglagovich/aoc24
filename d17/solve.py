class RegFile:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C
        self.pc = 0
    def __repr__(self):
        return f'pc={self.pc}\nA={self.A}\nB={self.B}\nC={self.C}'
# decode
# load operands
# ALU
# branch
# write back
# output
# increment PC
class Instr:
    def __init__(self, opcode, src0_val, src1_val, dst_ref):
        self.opcode = opcode
        self.src0_val = src0_val
        self.src1_val = src1_val
        self.dst_ref = dst_ref
    def __repr__(self):
        return f'Instr(opcode={self.opcode}, src0={self.src0_val}, src1={self.src1_val}, dst={self.dst_ref})'

op_code_to_name = ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv']
op_code_to_src0 = {
    'adv': 'A',
    'bxl': 'B',
    'bst': None,
    'jnz': 'A',
    'bxc': 'B',
    'out': None,
    'bdv': 'A',
    'cdv': 'A'
}
op_code_to_src1 = {
    'adv': 'combo',
    'bxl': 'literal',
    'bst': 'combo',
    'jnz': 'literal',
    'bxc': 'C',
    'out': 'combo',
    'bdv': 'combo',
    'cdv': 'combo'
}
op_code_to_dst = {
    'adv': 'A',
    'bxl': 'B',
    'bst': 'B',
    'jnz': 'pc',
    'bxc': 'B',
    'out': None,
    'bdv': 'B',
    'cdv': 'C'
}
op_code_to_alu = {
    'adv': lambda src0, src1: src0 // 2**src1,
    'bxl': lambda src0, src1: src0 ^ src1,
    'bst': lambda src0, src1: src1 % 8,
    'jnz': lambda src0, src1: None,
    'bxc': lambda src0, src1: src0 ^ src1,
    'out': lambda src0, src1: src1 % 8,
    'bdv': lambda src0, src1: src0 // 2**src1,
    'cdv': lambda src0, src1: src0 // 2**src1,
}

def decode(rf, program):
    '''
    Given the instruction at PC, return the source values and the dst location
    '''
    def eval_operand(rf, program, src_ref):
        combo_id_to_register = {4: 'A', 5: 'B', 6: 'C'}
        operand = program[rf.pc+1]
        if src_ref == 'combo':
            if operand <= 3:
                return operand
            return getattr(rf, combo_id_to_register[operand])
        if src_ref == 'literal':
            return operand
        if src_ref is None:
            return src_ref
        if src_ref in 'ABC':
            return getattr(rf, src_ref)
        assert False

    op_code = program[rf.pc]
    op = op_code_to_name[op_code]
    src0_ref = op_code_to_src0[op]
    src1_ref = op_code_to_src1[op]
    src0_val = eval_operand(rf, program, src0_ref)
    src1_val = eval_operand(rf, program, src1_ref)
    dst_ref = op_code_to_dst[op]
    return Instr(op, src0_val, src1_val, dst_ref)

def alu(instr):
    func = op_code_to_alu[instr.opcode]
    res = func(instr.src0_val, instr.src1_val)
    return res

def writeback(output, instr, rf, stdout):
    # Treat jnz and out separately
    did_branch = False
    if instr.opcode == 'jnz':
        if instr.src0_val != 0:
            rf.pc = instr.src1_val
            did_branch = True
    elif instr.opcode == 'out':
        stdout.append(output)
    else:
        setattr(rf, instr.dst_ref, output)
    return did_branch


def clk(rf, program, stdout):
    cur_instr = decode(rf, program)
    # print(cur_instr)
    output = alu(cur_instr)
    did_branch = writeback(output, cur_instr, rf, stdout)
    if not did_branch:
        rf.pc += 2


def test_adv():
    rf = RegFile(150, 3, 2)
    program = [0, 5]
    clk(rf, program, [])
    assert rf.A == 18 and rf.B == 3 and rf.C == 2 and rf.pc == 2

    rf = RegFile(150, 3, 2)
    program = [0, 2]
    clk(rf, program, [])
    assert rf.A == (150 // 2**2) and rf.B == 3 and rf.C == 2 and rf.pc == 2

def test_bxl():
    rf = RegFile(149, 150, 2)
    program = [1, 7]
    clk(rf, program, [])
    assert rf.A == 149 and rf.B == 150 ^ 7 and rf.C == 2 and rf.pc == 2

def test_bst():
    rf = RegFile(149, 150, 2)
    program = [2, 5]
    clk(rf, program, [])
    assert rf.A == 149 and rf.B == 150 % 8 and rf.C == 2 and rf.pc == 2, rf

    rf = RegFile(149, 150, 2)
    program = [2, 3]
    clk(rf, program, [])
    assert rf.A == 149 and rf.B == 3 % 8 and rf.C == 2 and rf.pc == 2, rf

def test_jnz():
    rf = RegFile(149, 150, 2)
    program = [3, 7]
    clk(rf, program, [])
    assert rf.A == 149 and rf.B == 150 and rf.C == 2 and rf.pc == 7, rf
    
    rf = RegFile(0, 150, 2)
    program = [3, 7]
    clk(rf, program, [])
    assert rf.A == 0 and rf.B == 150 and rf.C == 2 and rf.pc == 2, rf

def test_bxc():
    rf = RegFile(149, 150, 2)
    program = [4, 7]
    clk(rf, program, [])
    assert rf.A == 149 and rf.B == 150 ^ 2 and rf.C == 2 and rf.pc == 2, rf
    rf = RegFile(149, 150, 99)
    program = [4, 7]
    clk(rf, program, [])
    assert rf.A == 149 and rf.B == 150 ^ 99 and rf.C == 99 and rf.pc == 2, rf

def test_out():
    rf = RegFile(149, 150, 2)
    program = [5, 5]
    std_out = []
    clk(rf, program, std_out)
    assert rf.A == 149 and rf.B == 150 and rf.C == 2 and rf.pc == 2, rf
    assert std_out == [150 % 8]

    rf = RegFile(149, 150, 2)
    program = [5, 3]
    std_out = []
    clk(rf, program, std_out)
    assert rf.A == 149 and rf.B == 150 and rf.C == 2 and rf.pc == 2, rf
    assert std_out == [3 % 8]

def test_bdv():
    rf = RegFile(150, 3, 2)
    program = [6, 5]
    clk(rf, program, [])
    assert rf.A == 150 and rf.B == (150 // 2**3) and rf.C == 2 and rf.pc == 2, rf

    rf = RegFile(150, 3, 2)
    program = [6, 2]
    clk(rf, program, [])
    assert rf.A == 150 and rf.B == (150 // 2**2) and rf.C == 2 and rf.pc == 2

def test_cdv():
    rf = RegFile(150, 3, 2)
    program = [7, 5]
    clk(rf, program, [])
    assert rf.A == 150 and rf.B == 3 and rf.C == (150 // 2**3) and rf.pc == 2

    rf = RegFile(150, 3, 2)
    program = [7, 2]
    clk(rf, program, [])
    assert rf.A == 150 and rf.B == 3 and rf.C == (150 // 2**2) and rf.pc == 2
test_adv()
test_bxl()
test_bst()
test_jnz()
test_bxc()
test_out()
test_bdv()
test_cdv()


fname = 'input.txt'
init_rf, program = open(fname).read().split('\n\n')
A, B, C = list(map(lambda line: int(line[12:]), init_rf.split('\n')))
rf = RegFile(A, B, C)
program = list(map(lambda x: int(x), program[9:].split(',')))
print(rf)
print(program)
stdout = []
while True:
    try:
        clk(rf, program, stdout)
    except IndexError:
        break
print(stdout)
print(','.join([str(x) for x in stdout]))


def could_match(expected, test):
    if len(expected) < len(test):
        return False
    for t, e in zip(test, expected):
        if t != e:
            return False
    return True

# part 2
fname = 'input.txt'
init_rf, program = open(fname).read().split('\n\n')
A, B, C = list(map(lambda line: int(line[12:]), init_rf.split('\n')))
rf = RegFile(A, B, C)
program = list(map(lambda x: int(x), program[9:].split(',')))
print(rf)
print(program)
print(f'{len(program)=}')
found = False
a_init = 0
captured = 0
while True:
    if a_init % 100000 == 0:
        print(f'Testing {a_init}')
    if found:
        break
    stdout = []
    rf = RegFile(a_init, B, C)
    while True:
        try:
            clk(rf, program, stdout)
        except IndexError:
            break

    if stdout == program:
        print(a_init)
        found = True
    if ''.join(map(str, program)).endswith(''.join(map(str, stdout))):
        print(f'found {stdout}')
        a_init = 8 * a_init
    else:
        a_init += 1 