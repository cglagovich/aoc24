#part 1
s = [int(ss) for ss in open("input.txt").read().strip()]
print(s)

# naive way
disk = ['.'] * sum(s)
ptr = 0
blocks = s[::2]
free = s[1::2]
for idx, b in enumerate(blocks):
    for p in range(ptr, ptr + b):
        disk[p] = idx
    ptr += b
    if idx < len(free):
        ptr += free[idx]

# print(''.join([str(d) for d in disk]))

back_ptr = len(disk) - 1
front_ptr = 0
while 1:
    while back_ptr > 0 and disk[back_ptr] == '.':
        back_ptr -= 1
    while front_ptr < len(disk) and disk[front_ptr] != '.':
        front_ptr += 1
    if back_ptr < 0 or front_ptr >= len(disk) or front_ptr >= back_ptr:
        break
    disk[front_ptr] = disk[back_ptr]
    disk[back_ptr] = '.'
    # print(''.join([str(d) for d in disk]))

end = 0
while disk[end] != '.':
    end += 1

x = list(map(int, disk[:end]))

res = sum(map(lambda x: x[0] * x[1], zip(x, range(len(x)))))
print(res)


# part 2
from itertools import chain
def pretty(disk):
    print('|'.join([''.join(list(map(str, entry))) for entry in disk ]))
    # print(''.join(map(str, chain(*disk))))

def prettiest(disk):
    res = ''
    for entry in disk:
        if entry[1] == 'B':
            res += f'{entry[2]}'*entry[0]
        else:
            res += '.'*entry[0]
    print(res)
    return res

print(s)
alt = (["B", "F"] * (len(s)//2+1))[:len(s)]
values = list(chain(*zip(range(len(s)//2+1), range(len(s)//2+1))))
assert len(alt) == len(s)
disk = list(zip(s, alt, values))
print(disk)

back_ptr = len(disk) - 1

print('at the beginning')
prettiest(disk)
while back_ptr > 0:
    while back_ptr >= 0 and disk[back_ptr][1] == 'F':
        back_ptr -= 1
    # print(f'operating on disk[{back_ptr}]={disk[back_ptr]}')
    block = disk[back_ptr]
    bsz = block[0]
    bnum = block[2]
    for front_ptr in range(back_ptr):
        if disk[front_ptr][1] == 'B':
            continue
        if disk[front_ptr][0] >= bsz:
            # disk.pop(back_ptr)
            disk[back_ptr] = (bsz, 'F', 0)
            disk.insert(front_ptr, (bsz, 'B', bnum))
            disk[front_ptr+1] = (disk[front_ptr+1][0]-bsz, 'F')
            if disk[front_ptr+1][0] == 0:
                disk.pop(front_ptr+1)
            break
    back_ptr -= 1
    # prettiest(disk)
    # print(back_ptr)

res = prettiest(disk)

ans = 0
pos = 0
for b in disk:
    l = b[0]
    if b[1] != 'F':
        for p in range(pos, pos+l):
            ans += p * int(b[2])
    pos += l
    # if r != '.':
    #     ans += int(r) * v

print(ans)


    