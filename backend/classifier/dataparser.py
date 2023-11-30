import pandas as pd
from .requirement import Requirement, Annoation

SAMPLEIDINDEX = 1
DOCUMENTIDINDEX = 2
DOCTITLEINEDEX_SV = 3
DOCTITLEINEDEX_EN = 4
REQIDINDEX = 5
SECTITLEINDEX_SV = 6
SECTITLEINDEX_EN = 7
REQTEXTINDEX_SV = 8
REQTEXTINDEX_EN = 9
ADVICEINDEX_SV = 10
ADVICEINDEX_EN = 11
SPANINDEX = 12
TABLEINDEX_SB11 = 13
LABELINDEX_SB11 = 14
NAMEINDEX_SB11_EN = 15
NAMEINDEX_SB11_SV = 16
TABLEINDEX_CC = 17
LABELINDEX_CC = 18
NAMEINDEX_CC_EN = 19
NAMEINDEX_CC_SV = 20

DELIMITER = ";"


def parse_as_df(file_path, cs, table, lang):
    table = table.replace(" ", "-")
    dataset = parse(file_path)

    filter = lambda a: a.cs == cs and a.table == table and a.lang == lang
    reqs_with_annotation = [r for r in dataset if r.has_annotation(filter)]
    for r in reqs_with_annotation:
        r.filter_annotations(filter)

    df_dataset = pd.DataFrame([r.to_dictionary(lang) for r in reqs_with_annotation])
    return df_dataset


def parse(file_path, annotations_filter=None):
    dataset = []
    df_dataset = read(file_path)

    for row in df_dataset.values:
        reqId = row[REQIDINDEX]
        x = [i for (i, r) in enumerate(dataset) if r.req_id == reqId]
        if len(x) == 0:
            req = Requirement()
            req.req_id = reqId
            req.sample = row[SAMPLEIDINDEX]
            req.doc_id = row[DOCUMENTIDINDEX]
            req.doc_title_en = row[DOCTITLEINEDEX_EN]
            req.doc_title_sv = row[DOCTITLEINEDEX_EN]
            req.section_titles_en = row[SECTITLEINDEX_EN]
            req.section_titles_sv = row[SECTITLEINDEX_SV]
            req.req_text_en = row[REQTEXTINDEX_EN]
            req.req_text_sv = row[REQTEXTINDEX_SV]
            req.advice_en = row[ADVICEINDEX_EN]
            req.advice_sv = row[ADVICEINDEX_SV]

            parse_annotations(row, req)

            dataset.append(req)

        else:
            parse_annotations(row, dataset[x[0]])

    if annotations_filter:
        print("filtering annotations")
        reqs_with_annotation = [
            r for r in dataset if r.has_annotation(annotations_filter)
        ]

        for r in reqs_with_annotation:
            r.filter_annotations(annotations_filter)

        return reqs_with_annotation

    return dataset


def read(file_path):
    df_dataset = pd.read_csv(file_path, delimiter=DELIMITER, keep_default_na=False)
    return df_dataset


def parse_annotations(row, req):
    cond = (
        lambda a: a.lang == a_en.lang
        and a.label == a_en.label
        and a.table == a_en.table
        and a.cs == a_en.cs
    )

    if row[TABLEINDEX_SB11] != None and row[TABLEINDEX_SB11] != "":
        tables = row[TABLEINDEX_SB11].strip().split("#")
        labels = row[LABELINDEX_SB11].strip().split("#")
        name_en = row[NAMEINDEX_SB11_EN].strip().split("#")
        name_sv = row[NAMEINDEX_SB11_EN].strip().split("#")
        for t, l, n_en, n_sv in zip(tables, labels, name_en, name_sv):
            a_en = Annoation(row[SPANINDEX], "en", "SB11", t, l, n_en)
            if not req.has_annotation(cond):
                req.annotations.append(a_en)

            a_sv = Annoation(row[SPANINDEX], "sv", "SB11", t, l, n_sv)
            if not req.has_annotation(cond):
                req.annotations.append(a_sv)

    if row[TABLEINDEX_CC] != None and row[TABLEINDEX_CC] != "":
        tables = row[TABLEINDEX_CC].strip().split("#")
        labels = row[LABELINDEX_CC].strip().split("#")
        name_en = row[NAMEINDEX_CC_EN].strip().split("#")
        name_sv = row[NAMEINDEX_CC_SV].strip().split("#")
        for t, l, n_en, n_sv in zip(tables, labels, name_en, name_sv):
            a_en = Annoation(row[SPANINDEX], "en", "CoClass", t, l, n_en)
            if not req.has_annotation(cond):
                req.annotations.append(a_en)

            a_sv = Annoation(row[SPANINDEX], "sv", "CoClass", t, l, n_sv)
            if not req.has_annotation(cond):
                req.annotations.append(a_sv)


def append_unique_annotation(req, annotation):
    if not req.has_annotation(
        lambda a: a.annotations == annotation.lang
        and a.label == annotation.label
        and a.table == annotation.table
        and a.annotations.cs == annotation.cs
    ):
        req.annotations.append(req)
