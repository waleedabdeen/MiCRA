import json

classifier_config = {
    "k": 5,
    "model": "all-MiniLM-L12-v2",
    "lower_case": True,
    "embedding": "sentence",
    "cs": "CoClass",
    "dimension": "Tillgångssystem",
    "lang": "en",
    "hierarchy": "bottomup",
    #'doubletap': False,
    "cutoff": 0.30,
}


def read_config():
    file_pah = "config.json"
    with open(file_pah, "r") as config_file:
        return json.load(config_file)
