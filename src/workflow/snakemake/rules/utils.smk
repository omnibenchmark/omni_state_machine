import pickle

def load_benchmark(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)