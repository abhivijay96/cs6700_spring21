end_states = set()

with open('points.txt', 'r') as points_file:
    line = points_file.readline()
    while line:
        line = line.strip()
        if line.startswith('['):
            line = points_file.readline()
            continue
        parts = line.split('|')
        end_states.add(line)
        line = points_file.readline()

print(len(end_states))