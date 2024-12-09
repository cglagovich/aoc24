# part 1
lines = open('input.txt').readlines()

'''
How do you hit all possible combinations of operators in a list?
There are 2**n number of combinations
+++++
++++*
+++*+
+++**
++*++
++*+*
++**+
++***
'''
le = 4
def perm(le):
    val = ['+'] * le
    yield val
    while not all(v == '*' for v in val):
        for idx in reversed(range(le)):
            if val[idx] == '*':
                val[idx] = '+'
            elif val[idx] == '+':
                val[idx] = '*'
                break
        yield val
from tqdm import tqdm
total = 0
for l in lines:
    t, s = l.split(':')
    t = int(t)
    s = list(map(int, s.strip().split()))
    for p in perm(len(s)-1):
        res = s[0]
        worked = False
        for idx, op in enumerate(p):
            if op == '+':
                res = res + s[idx+1]
            else:
                res = res * s[idx+1]
            if res == t:
                total += t
                worked = True
                break
        if worked:
            break
print(total)

# part 2
'''
+++
++*
++|
+*+
+**
+*|
+|+
+|*
+||
*++
*+*
*+|
**+
***
**|
*|+
*|*
*||

...

'''
def perm(le):
    val = ['+'] * le
    yield val
    while not all(v == '|' for v in val):
        for idx in reversed(range(le)):
            if val[idx] == '|':
                val[idx] = '+'
            elif val[idx] == '+':
                val[idx] = '*'
                break
            elif val[idx] == '*':
                val[idx] = '|'
                break
        yield val

total = 0
for idx, l in tqdm(enumerate(lines)):
    t, s = l.split(':')
    t = int(t)
    s = list(map(int, s.strip().split()))
    for p in perm(len(s)-1):
        res = s[0]
        worked = False
        for idx, op in enumerate(p):
            if op == '+':
                res = res + s[idx+1]
            elif op == '*':
                res = res * s[idx+1]
            elif op == '|':
                res = int(str(res) + str(s[idx+1]))
            else:
                assert False
        if res == t:
            total += t
            worked = True
            break
        if worked:
            break
print(total)