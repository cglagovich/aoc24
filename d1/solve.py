# part 1
print(sum(map(lambda x: max(x[0], x[1]) - min(x[0], x[1]), zip(*[sorted([int(l[i]) for l in [l.split() for l in open("input.txt").readlines()]]) for i in range(2)]))))

# part 2
print(sum([ll for l in [[[int(l[i]) for l in [l.split() for l in open("input.txt").readlines()]] for i in range(2)]] for ll in l[1] if ll in l[0]]))