# part 1
print(sum([all(map(lambda x: x*sign >= 1 and x*sign <= 3, [l[i] - l[i+1] for i in range(len(l)-1)])) for l in [list(map(int, line.split())) for line in open("input.txt").readlines()] for sign in (1, -1)]))

# part 2
