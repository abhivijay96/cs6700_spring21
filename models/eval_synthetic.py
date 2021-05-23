from tensorflow.keras.models import save_model, load_model
import pickle, sys, random

random.seed(1995)

model_name = sys.argv[1]
pkl_file = sys.argv[2]

model = load_model(model_name)
print('Loaded model', model_name)
print('Pickle file to load', pkl_file)

with open(pkl_file, 'rb') as f:
    examples = pickle.load(f)
    print('Loaded examples')
    random.shuffle(examples)
    sample = examples[: 100000]
    # print(sample[0])
    print(model.evaluate(sample, [0 for _ in range(len(sample))]))



