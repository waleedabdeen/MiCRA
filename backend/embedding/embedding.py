import os
import pickle


def try_read_taxonomy_embedding(cs, dimension):
    file = f"{cs}_{dimension}.rb"
    exists = os.path.exists(file)
    if not exists:
        return None

    with open(file, "rb") as f:
        embedding = pickle.load(f)
        return embedding


def save_embedding(embedding, cs, dimension):
    file = f"{cs}_{dimension}.rb"
    with open(file, "wb") as f:
        pickle.dump(embedding, f)
