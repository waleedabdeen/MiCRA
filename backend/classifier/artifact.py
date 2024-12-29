import json

class Artifact:
    def __init__(self):
        self.id = 0
        self.text = ""
        self.type = ""
        self.labels = []

    def __str__(self):
        return f"id: {self.id}, text: {self.text}, type: {self.type}, labels: {self.labels}"

    def toArray(self):
        result = []
        result.append(self.sample)
        result.append(self.req_id)
        result.append(self.doc_id)
        result.append(self.doc_title_en)
        result.append(self.doc_title_sv)
        result.append(self.section_titles_en)
        result.append(self.section_titles_sv)
        result.append(self.req_text_en)
        result.append(self.req_text_sv)
        result.append(self.advice_en)
        result.append(self.advice_sv)
        result.append(self.annotaitons)
        return result

    def has_labels(self, condition=None):
        if condition != None:
            print('filtering')
            print(self.labels)
            print(condition)
            return any(a for a in self.labels if condition(a))
        
        return any(self.labels)


    def to_dictionary(self):
        return {
            "id": self.id,
            "text": self.text.replace("\n", " "),
            "type": self.type,
            "labels": self.labels,
            "label_str": str.join(",", [a['label'] for a in self.labels],
            ),
            "label_name": [a['label_name'] for a in self.labels],
        }

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
