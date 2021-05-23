import pandas as pd

positive_size_default = 0.5
negative_size_default = 0.5
layer_count_default = 1
neuron_count_default = 18

positive_sizes = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
negative_sizes = [0.25, 0.5, 0.75]
layer_counts = [1, 2, 3]
neuron_counts = []

for i in range(1, 13):
    neuron_counts.append(i * 3)

pkl_files = ['many_moves.pkl', 'overwrite.pkl', 'wrong_symbol.pkl']

def get_lines(file_name):
    lines = None
    with open(file_name, 'r') as log_file:
        lines = log_file.readlines()
    return lines

def get_synth_accuracy(log_file_name):
    lines = get_lines(log_file_name)
    last_line = lines[-1]
    last_line = last_line.strip()
    last_line = last_line.replace('[', '').replace(']', '')
    return float(last_line.split(',')[1].strip())

def get_train_accuracy(log_file_name):
    lines = get_lines(log_file_name)
    last_line = lines[-1]
    assert 'val_accuracy' in last_line
    return float(last_line.split()[-1].strip())

def plot_log(positive_size, negative_size, neurons, layers, y_val, ys):
    name_list = ['model', positive_size, negative_size, neurons, layers]
    for idx in range(len(name_list)):
        name_list[idx] = str(name_list[idx])
    model_name = '_'.join(name_list)
    model_name = model_name.replace('.', 'dot')
    log_file_name = model_name + '.log'
    print('Getting train accuracy for', log_file_name)
    y_val.append(get_train_accuracy(log_file_name))

    for idx in range(len(pkl_files)):
        log_file_name_prefix = model_name + '_es_' + pkl_files[idx].split('.')[0] 
        log_file_name = log_file_name_prefix + '.log'
        print('Getting synth accuracy for', log_file_name)
        ys[idx].append(get_synth_accuracy(log_file_name))



def print_tsv(val_lists, headers):
    result = {}
    for idx in range(len(headers)):
        result[headers[idx]] = val_lists[idx]
    df = pd.DataFrame(result)
    df.to_csv('test.tsv', sep='\t', index=False) 


# xs = [0.1]
# y_vals = []
# y_many = []
# y_overwrite = []
# y_wrong = []
# plot_log(0.1, negative_size_default, neuron_count_default, layer_count_default, y_vals, [y_many, y_overwrite, y_wrong])
# print(xs, y_vals, y_many, y_wrong, y_overwrite)

xs = []
y_vals = []
y_many = []
y_overwrite = []
y_wrong = []
## varying just positive sizes
for size in positive_sizes:
    xs.append(float(size))
    plot_log(size, negative_size_default, neuron_count_default, layer_count_default, y_vals, [y_many, y_overwrite, y_wrong])

print_tsv([xs, y_vals, y_many, y_overwrite,y_wrong], ['Positive fraction', 'Val accuracy', 'Many accuracy', 'Overwrite accuracy', 'Wrong accuracy'])

# ## varying negative sizes
# for size in negative_sizes:
#     plot_log(positive_size_default, size, neuron_count_default, layer_count_default)

# ## varying number of layers
# for layer_count in layer_counts:
#     plot_log(positive_size_default, negative_size_default, neuron_count_default, layer_count)

# ## varying number of neurons
# for neuron_count in neuron_counts:
#     plot_log(positive_size_default, negative_size_default, neuron_count, layer_count_default)