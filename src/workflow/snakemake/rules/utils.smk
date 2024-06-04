import pickle

def load(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)