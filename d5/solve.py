# part 1
inp = open("input.txt").readlines()
rules = []
lines = []
in_rules = True
for l in inp:
    if l == '\n':
        in_rules = False
        continue
    if in_rules:
        rules.append(list(map(int, l.strip().split('|'))))
    else:
        lines.append(list(map(int, l.strip().split(','))))

print(rules[0])
print(rules[-1])
print(lines[0])
print(lines[-1])

res = 0
for l in lines:
    good = True
    for r in rules:
        if not (r[0] in l and r[1] in l):
            continue
        if l.index(r[1]) < l.index(r[0]):
            good = False
            break
    if good:
        res += l[len(l)//2]

print(res)

# part 2
res = 0
for l in lines:
    good = True
    for r in rules:
        if not (r[0] in l and r[1] in l):
            continue
        if l.index(r[1]) < l.index(r[0]):
            good = False
            break
    if not good:
        # Sort it according to rules
        lcopy = l.copy()
        failing = True
        while failing:
            failing = False
            for r in rules:
                if not (r[0] in lcopy and r[1] in lcopy):
                    continue
                if lcopy.index(r[1]) < lcopy.index(r[0]):
                    old_index = lcopy.index(r[1])
                    lcopy.insert(lcopy.index(r[0])+1, r[1])
                    lcopy.pop(old_index)
                    failing = True
        res += lcopy[len(lcopy)//2]

print(res)