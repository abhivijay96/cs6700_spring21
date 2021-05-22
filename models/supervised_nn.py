import random
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import save_model, load_model
import json
import os
import pickle

tf.random.set_seed(1996)

positive_examples = []
neagative_examples = []
fraction_data_for_train = 1

positive_type = 1
negative_type = 2

positive_label = 1
negative_label = 0

positive_idx = 0
negative_idx = 0

positive_txt_path = '../dataset/positive.txt'
negative_txt_path = '../dataset/negative.txt'
positive_json_path = 'positive.json'
negative_json_path = 'negative.json'

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

def popoulate_samples(size, samples, labels):
    global negative_idx
    global positive_idx
    for _ in range(0, int(size)):
        point_type = random.choice([negative_type, positive_type])
        
        if point_type == positive_type:
            samples.append(positive_examples[positive_idx])
            labels.append(positive_label)
            positive_idx += 1

        if point_type == negative_type:
            samples.append(neagative_examples[negative_idx])
            labels.append(negative_label)
            negative_idx += 1

def store_json(target, file_name):
    with open(file_name, 'w') as file_handle:
        file_handle.write(json.dumps(target))
        file_handle.flush()

def gen_data_points(json_path, txt_path, point_type):
    global positive_examples
    global neagative_examples
    examples = positive_examples if point_type == positive_type else neagative_examples
    if not os.path.exists(json_path):
        populate_data_points(txt_path, examples)
        store_json(examples, json_path)
    else:
        data = None
        with open(json_path, 'r') as json_file:
            data = json.loads(json_file.read())
        if point_type == positive_type:
            positive_examples = data
        else:
            neagative_examples = data

def get_pkl_examples(filename):
    with open(filename, 'rb') as f:
        examples = pickle.load(f)
        return examples

print('loading positive data points')
gen_data_points(positive_json_path, positive_txt_path, positive_type)
print('loading negative data points')
gen_data_points(negative_json_path, negative_txt_path, negative_type)
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



training_set_size = fraction_data_for_train * len(positive_examples)
print('Training set size: ', training_set_size)
popoulate_samples(training_set_size, training_samples, training_labels)
assert len(training_samples) == int(training_set_size)

validation_set_size = training_set_size / 10
print('Validation set size: ', validation_set_size)
popoulate_samples(validation_set_size, validation_samples, validation_labels)
assert len(validation_samples) == int(validation_set_size)

game_model = tf.keras.Sequential(
    [layers.Dense(18, activation='relu'),
    layers.Dense(1, activation='sigmoid')]) # change this to modify the number of layers
game_model.compile(loss='binary_crossentropy', optimizer = tf.optimizers.Adam(), metrics=['accuracy'])

game_model.fit(training_samples, training_labels, epochs=250, validation_data=(validation_samples, validation_labels))
save_model(game_model, 'model')