import os
from dotenv import load_dotenv

classifier_config = {
    "k": 5,
    "model": "all-MiniLM-L12-v2",
    "lower_case": True,
    "embedding": "sentence",
    "cs": "Tele",
    "dimension": "Chatgpt",
    "lang": "en",
    "hierarchy": "bottomup",
    #'doubletap': False,
    "cutoff": 0.30,
}


def read_env_vars():
    load_dotenv()
    OUTPUT = os.getenv("OUTPUT")
    LLAMA_MODELS = os.getenv("LLAMA_MODELS")
    COCLASS = os.getenv("COCLASS")
    SB11 = os.getenv("SB11")
    TELE = os.getenv("TELE")
    DATA = os.getenv("DATA")
    SERVER_ENV = os.getenv("SERVER_ENV")

    env_vars = {
        "output": OUTPUT,
        "CoClass": COCLASS,
        "SB11": SB11,
        "Tele": TELE,
        "data": DATA,
        "server_env": SERVER_ENV,
    }
    return env_vars
