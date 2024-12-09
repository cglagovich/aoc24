# part 1
import re
lines = open("input.txt").read()
matches = re.findall("mul\([0-9]*,[0-9]*\)", lines)
r = [list(map(int, m.split('(')[1].split(')')[0].split(','))) for m in matches]
r = list(map(lambda x: x[0] * x[1], r))
print(sum(r))

# part 2
lines = open("input.txt").read()
# stops = re.findall("don't\(\_)", lines)
# starts = re.findall("do\(\)")
# for stop in stops:

while "don't()" in lines:
    start = lines.index("don't")
    if "do()" in lines:
        end = lines.index("do()")
        print(start, end)
        if end > start:
            # Remove span from don't to do
            print(start,end)
            lines = lines[:start] + lines[end+4:]
        if start > end:
            # Remove do
            lines = lines[:end] + lines[end+4:]
    else:
        # Remove everything after don't
        lines = lines[:start]
        break

matches = re.findall("mul\([0-9]*,[0-9]*\)", lines)

while removes := re.search("don\'t\(\).*?do\(\)", lines):
    lines = lines[:removes.start()] + lines[removes.end():]

matches = re.findall("mul\([0-9]*,[0-9]*\)", lines)
r = [list(map(int, m.split('(')[1].split(')')[0].split(','))) for m in matches]
r = list(map(lambda x: x[0] * x[1], r))
print(sum(r))

# r = [list(map(int, m.split('(')[1].split(')')[0].split(','))) for m in matches]
# r = list(map(lambda x: x[0] * x[1], r))
# print(sum(r))