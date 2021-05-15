from tensorflow.keras.models import save_model, load_model
import pickle, sys, random

model = load_model('model')
print('Loaded model')

with open(sys.argv[1], 'rb') as f:
    examples = pickle.load(f)
    print('Loaded examples')
    random.shuffle(examples)
    sample = examples[:100000]
    print(sample[0])
    print(model.evaluate(sample, [0 for _ in range(len(sample))]))



