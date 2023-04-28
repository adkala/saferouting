import pickle

DEFAULT_FILE_PATH = ".serialized_routes"


def save(routes, filepath: str = DEFAULT_FILE_PATH):
    with open(filepath, "wb") as outp:
        pickle.dump(routes, outp, pickle.HIGHEST_PROTOCOL)


def load(filepath: str = DEFAULT_FILE_PATH):
    with open(filepath, "rb") as inp:
        return pickle.load(inp)
