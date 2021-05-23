import random

def is_valid_move(current_state, next_state):
    current_parts = str(current_state).split(',')
    next_parts = str(next_state).split(',')
    # print(current_parts)
    # print(next_parts)
    assert len(current_parts) == len(next_parts)
    changed_count = 0
    new_count = 0
    num_xs = len([c for c in current_parts if c == '1'])
    num_os = len([c for c in current_parts if c == '-1'])
    correct_move = None
    if(num_xs == num_os):
        correct_move = '1'
    else:
        correct_move = '-1'
    shape = None
    for idx in range(len(current_parts)):
        if current_parts[idx] == '0' and next_parts[idx] != '0':
            new_count += 1
            shape = next_parts[idx]
        elif current_parts[idx] != '0' and next_parts[idx] != current_parts[idx]:
            # print('idx', idx, 'curr', current_parts[idx], 'next', next_parts[idx])
            changed_count += 1
    return changed_count == 0 and new_count == 1 and shape == correct_move

def gen_next_state(current_valid_state):
    new_state = []
    change = 0
    no_change = 1
    entries = str(current_valid_state).split(',')
    for entry in entries:
        should_change = True if random.choice([change, no_change]) == change else False
        new_entry = entry
        if should_change:
            new_entry = random.choice([-1, 1, 0])
        new_state.append(str(new_entry))
    return ','.join(new_state)
    

with open('positive.txt', 'r') as file_handle:
    line = file_handle.readline()
    while line:
        line = line.strip()
        parts = line.split('|')
        current_valid_state = parts[0]
        # print(current_valid_state)
        new_state = gen_next_state(current_valid_state)
        # print(new_state)
        if not is_valid_move(current_valid_state, new_state):
            print(current_valid_state + '|' + new_state)
        line = file_handle.readline()