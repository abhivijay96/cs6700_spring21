import random
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import save_model
import json
import sys
import pickle

tf.random.set_seed(1996)

if len(sys.argv) < 5:
    print('Invalid argument count', len(sys.argv))
    exit(0)
print(sys.argv)
fraction_positive_data = float(sys.argv[1])
fractin_negative_data = float(sys.argv[2])
neuron_count = int(sys.argv[3])
layer_count = int(sys.argv[4])
model_name = sys.argv[5]

print('Positive fraction passed', fraction_positive_data)
print('Negative fraction passed', fractin_negative_data)
print('Neuron count passed', neuron_count)
print('Layer count passed', layer_count)
print('Model name passed', model_name)

positive_examples = []
neagative_examples = []

positive_type = 1
negative_type = 2

positive_label = 1
negative_label = 0

positive_idx = 0
negative_idx = 0

positive_txt_path = '../dataset/positive.txt'
negative_txt_path = '../dataset/negative.txt'

def convert_string_to_list(board_state):
    result = []
    entries = str(board_state).split(',')
    for entry in entries:
        result.append(int(entry))
    return result

def populate_data_points(file_name, target):
    with open(file_name, 'r') as file_handle:
        line = file_handle.readline()
        while line:
            line = line.strip()
            parts = line.split('|')
            current_state_str = parts[0]
            next_state_str = parts[1]
            current_state = convert_string_to_list(current_state_str)
            next_state = convert_string_to_list(next_state_str)
            current_state.extend(next_state)
            target.append(current_state)
            line = file_handle.readline()

def popoulate_samples(positive_size, negative_size, samples, labels):
    global negative_idx
    global positive_idx
    positive_size = int(positive_size)
    negative_size = int(negative_size)

    for _ in range(0, positive_size):
        labels.append(positive_label)
    for _ in range(0, negative_size):
        labels.append(negative_label)
    
    random.shuffle(labels)

    for label in labels:
        if label == positive_label:
            samples.append(positive_examples[positive_idx])
            positive_idx += 1
        if label == negative_label:
            samples.append(neagative_examples[negative_idx])
            negative_idx += 1

def store_json(target, file_name):
    with open(file_name, 'w') as file_handle:
        file_handle.write(json.dumps(target))
        file_handle.flush()

def gen_data_points(txt_path, point_type):
    global positive_examples
    global neagative_examples
    examples = positive_examples if point_type == positive_type else neagative_examples
    # if not os.path.exists(json_path):
    populate_data_points(txt_path, examples)
    # store_json(examples, json_path)
    # else:
    #     data = None
    #     with open(json_path, 'r') as json_file:
    #         data = json.loads(json_file.read())
    #     if point_type == positive_type:
    #         positive_examples = data
    #     else:
    #         neagative_examples = data

def get_pkl_examples(filename):
    with open(filename, 'rb') as f:
        examples = pickle.load(f)
        return examples

print('loading positive data points')
gen_data_points(positive_txt_path, positive_type)
print('loading negative data points')
gen_data_points(negative_txt_path, negative_type)
# neagative_examples = []
# neagative_examples.extend(get_pkl_examples('../dataset/wrong_symbol.pkl'))
# neagative_examples.extend(get_pkl_examples('../dataset/overwrite.pkl'))
# neagative_examples.extend(get_pkl_examples('../dataset/many_moves.pkl'))

training_samples = []
training_labels = []

validation_samples = []
validation_labels = []

random.shuffle(positive_examples)
random.shuffle(neagative_examples)


positive_size = fraction_positive_data * len(positive_examples)
negative_size = fraction_positive_data * len(positive_examples)
print('Positive train set size:', positive_size)
print('Negative train set size:', negative_size)

training_set_size = positive_size + negative_size
print('Training set size: ', training_set_size)
popoulate_samples(positive_size, negative_size, training_samples, training_labels)
assert len(training_samples) == int(positive_size) + int(negative_size)

validation_set_size = training_set_size / 10
pos_validation_set_size = validation_set_size / 2
neg_validation_set_size = pos_validation_set_size
print('Validation set size: ', validation_set_size)
print('Positive val set size:', pos_validation_set_size)
print('Negative val set size:', neg_validation_set_size)

popoulate_samples(pos_validation_set_size, neg_validation_set_size, validation_samples, validation_labels)
assert len(validation_samples) == int(pos_validation_set_size) + int(neg_validation_set_size)

layer_list = []
for _ in range(0, layer_count):
    layer_list.append(layers.Dense(neuron_count, activation='relu'))

layer_list.append(layers.Dense(1, activation='sigmoid'))

game_model = tf.keras.Sequential(layer_list)
game_model.compile(loss='binary_crossentropy', optimizer = tf.optimizers.Adam(), metrics=['accuracy'])

game_model.fit(training_samples, training_labels, epochs=150, validation_data=(validation_samples, validation_labels))
save_model(game_model, model_name)