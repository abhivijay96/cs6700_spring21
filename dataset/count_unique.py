import sys

seen_lines = set()

with open(sys.argv[1], 'r') as read_file:
    for line in read_file:
        line = line.strip()
        seen_lines.add(line)

print('Unique number of data points in', sys.argv[1], len(seen_lines))