import random
import pickle
    
def gen_wrong_symbol(cur_state):
    entries = str(cur_state).split(',')
    empty_positions = [i for i in range(len(entries)) if entries[i] == '0']
    if(len(empty_positions) == 0):
        return None
    
    num_xs = len([x for x in entries if x == '1'])
    num_os = len([x for x in entries if x == '-1'])
    new_entry = '-1' if num_xs == num_os else '1' # Is X == 1?

    pos = random.choice(empty_positions)
    new_state = entries[:]
    new_state[pos] = new_entry
    return new_state


def gen_overwrite(cur_state):
    entries = str(cur_state).split(',')
    filled_positions = [i for i in range(len(entries)) if entries[i] != '0']
    if(len(filled_positions) == 0):
        return None
    
    pos = random.choice(filled_positions)

    num_xs = len([x for x in entries if x == '1'])
    num_os = len([x for x in entries if x == '-1'])
    new_entry = '1' if num_xs == num_os else '-1'

    pos = random.choice(filled_positions)
    new_state = entries[:]
    new_state[pos] = new_entry
    return new_state


def gen_many_moves(cur_state):
    entries = str(cur_state).split(',')
    empty_positions = [i for i in range(len(entries)) if entries[i] == '0']
    if(len(empty_positions) < 2):
        return None

    positions = random.sample(empty_positions, random.choice(range(2, len(empty_positions) + 1)))

    num_xs = len([x for x in entries if x == '1'])
    num_os = len([x for x in entries if x == '-1'])
    new_entry = '1' if num_xs == num_os else '-1'

    new_state = entries[:]
    for pos in positions:
        new_state[pos] = new_entry
    
    return new_state

def gen_examples(inp_file, out_file, gen_func):
    examples = []
    with open(inp_file, 'r') as file_handle:
        line = file_handle.readline()
        count  = 0
        while line:
            line = line.strip()
            parts = line.split('|')
            current_valid_state = parts[0]
            cur_state = current_valid_state.split(',')
            # print(current_valid_state)
            new_state = gen_func(current_valid_state)
            if new_state == None:
                line = file_handle.readline()
                continue
            example = cur_state + new_state
            examples.append([int(a) for a in example])
            count += 1
            if(count % 100000 == 0):
                print(count)
            # outf.write(current_valid_state + '|' + new_state + '\n')
            line = file_handle.readline()
    
    with open(out_file, 'wb') as f:
        pickle.dump(examples, f)

random.seed(1996)

gen_examples('positive.txt', 'wrong_symbol.pkl', gen_wrong_symbol)
print('done')
gen_examples('positive.txt', 'overwrite.pkl', gen_overwrite)
print('done')
gen_examples('positive.txt', 'many_moves.pkl', gen_many_moves)
print('done')