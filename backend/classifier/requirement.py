import json


class Annoation:
    def __init__(self, span, lang, cs, table, label, name) -> None:
        self.span = span
        self.lang = lang
        self.cs = cs
        self.table = table
        self.label = label
        self.label_name = name

    def __repr__(self):
        return f"span: {self.span}, lang: {self.lang}, cs: {self.cs}, table: {self.table}, label: {self.label}, name: {self.label_name}."

    def __str__(self):
        return f"span: {self.span}, lang: {self.lang}, cs: {self.cs}, table: {self.table}, label: {self.label}, name: {self.label_name}."


class Requirement:
    def __init__(self):
        self.sample = 0
        self.req_id = ""
        self.doc_id = ""
        self.doc_title_en = ""
        self.doc_title_sv = ""
        self.section_titles_en = ""
        self.section_titles_sv = ""
        self.req_text_en = ""
        self.req_text_sv = ""
        self.advice_en = ""
        self.advice_sv = ""
        self.annotations = []

    def __repr__(self):
        return f"sample: {self.sample}, id: {self.req_id}, doc_id: {self.doc_id}, doc title (en): {self.doc_title_en}, doc title (sv): {self.doc_title_sv}, section titles (en): {self.section_titles_en}, section titles (sv): {self.section_titles_sv}, text (en): {self.req_text_en}, text (sv): {self.req_text_sv}"

    def __str__(self):
        return f"sample: {self.sample}, id: {self.req_id}, doc_id: {self.doc_id}, doc title (en): {self.doc_title_en}, doc title (sv): {self.doc_title_sv}, section titles (en): {self.section_titles_en}, section titles (sv): {self.section_titles_sv}, text (en): {self.req_text_en}, text (sv): {self.req_text_sv}"

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

    def has_annotation(self, condition=None):
        return any(a for a in self.annotations if condition(a))

    def filter_annotations(self, filter=None):
        self.annotations = [a for a in self.annotations if filter(a)]
        return self.annotations

    def to_dictionary(self, lang):
        return {
            "req_id": self.req_id,
            "doc_id": self.doc_id,
            "doc_title": self.doc_title_en if lang == "en" else self.doc_title_sv,
            "section_titles": self.section_titles_en
            if lang == "en"
            else self.section_titles_sv,
            "req_text": self.req_text_en if lang == "en" else self.req_text_sv,
            "advice_en": self.advice_en if lang == "en" else self.advice_sv,
            "label_str": str.join(
                ",",
                [a.label for a in self.filter_annotations(lambda a: a.lang == lang)],
            ),
            "label": [
                a.label for a in self.filter_annotations(lambda a: a.lang == lang)
            ],
            "label_name": [a.label_name for a in self.annotations],
        }

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
