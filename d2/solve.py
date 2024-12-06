# part 1
print(sum([all(map(lambda x: x*sign >= 1 and x*sign <= 3, [l[i] - l[i+1] for i in range(len(l)-1)])) for l in [list(map(int, line.split())) for line in open("input.txt").readlines()] for sign in (1, -1)]))

# part 2
lines = open("input.txt").readlines()
n = 0
for l in lines:
    l = list(map(int, l.split()))
    def is_valid(l):
        diff = [l[i] - l[i+1] for i in range(len(l)-1)]
        up = list(map(lambda x: -x >= 1 and -x <= 3, diff))
        down = list(map(lambda x: x >= 1 and x <= 3, diff))
        valid = all(up) or all(down)
        return valid
    any_valid = any([is_valid(l)] + [is_valid(l[:i]+l[i+1:]) for i in range(len(l))])
    if any_valid:
        n +=1 
print(n)


ret = [[all(map(lambda x: x*sign >= 1 and x*sign <= 3, [l[i] - l[i+1] for i in range(len(l)-1) if i != skip])) for l in [list(map(int, line.split())) for line in open("input.txt").readlines()] for sign in (1, -1)] for skip in range(-1, len(l))]
print(len(ret))