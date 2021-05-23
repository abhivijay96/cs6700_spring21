# python3 supervised_nn.py pos_size neg_size neurons layers model_1
# python3 eval_synthetic.py model_name pickle_file_path
# python3 supervised_nn.py 0.5 0.5 18 1 model_1

import subprocess
import os

positive_size_default = 0.5
negative_size_default = 0.5
layer_count_default = 1
neuron_count_default = 18

positive_sizes = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
negative_sizes = [0.25, 0.5, 0.75]
layer_counts = [1, 2, 3]
pkl_files = ['../dataset/many_moves.pkl', '../dataset/overwrite.pkl', '../dataset/wrong_symbol.pkl']
neuron_counts = []

for i in range(1, 13):
    neuron_counts.append(i * 3)

def write_to_file(file_name, data):
    with open(file_name, 'w') as log_file:
        log_file.write(data)

def run_nnet(positive_size, negative_size, neurons, layers):
    name_list = ['model', positive_size, negative_size, neurons, layers]
    for idx in range(len(name_list)):
        name_list[idx] = str(name_list[idx])
    model_name = '_'.join(name_list)
    model_name = model_name.replace('.', 'dot')
    log_file_name = model_name + '.log'
    err_file_name = model_name + '_err.log'

    print('Running model:', model_name)
    # train and validate
    result = subprocess.run(['python3', 'supervised_nn.py', str(positive_size), str(negative_size), str(neurons), str(layers), model_name], capture_output=True)
    write_to_file(log_file_name, result.stdout.decode())
    write_to_file(err_file_name, result.stderr.decode())

    # synthetic validate
    for pkl_file in pkl_files:
        pkl_file_name = os.path.basename(pkl_file)
        log_file_name_prefix = model_name + '_es_' + pkl_file_name.split('.')[0] 
        log_file_name = log_file_name_prefix + '.log'
        err_file_name = log_file_name_prefix + '_err.log'
        print('Running eval', log_file_name_prefix)
        result = subprocess.run(['python3', 'eval_synthetic.py', model_name, pkl_file], capture_output=True)
        write_to_file(log_file_name, result.stdout.decode())
        write_to_file(err_file_name, result.stderr.decode())

## varying just positive sizes
for size in positive_sizes:
    run_nnet(size, negative_size_default, neuron_count_default, layer_count_default)

## varying negative sizes
for size in negative_sizes:
    run_nnet(positive_size_default, size, neuron_count_default, layer_count_default)

## varying number of layers
for layer_count in layer_counts:
    run_nnet(positive_size_default, negative_size_default, neuron_count_default, layer_count)

## varying number of neurons
for neuron_count in neuron_counts:
    run_nnet(positive_size_default, negative_size_default, neuron_count, layer_count_default)