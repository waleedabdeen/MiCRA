## for config
from classifier.gpu import config_gpu
from classifier.configurations import read_env_vars

## for data
import pandas as pd
import numpy as np
from sklearn import metrics, manifold
import classifier.dataparser as dataparser
from classifier.taxonomy_aggregator import aggregate_nodes, remove_dummy_nodes

## for processing
import re
import nltk

## for plotting
import matplotlib.pyplot as plt
import seaborn as sns

## models
import tensorflow as tf
from sentence_transformers import SentenceTransformer
import torch.nn.functional as F
import time
from embedding.embedding import try_read_taxonomy_embedding, save_embedding

##logging
import logging


class ZSC:
    def __init__(self, ex):
        config_gpu()
        nltk.download("stopwords")
        nltk.download("wordnet")
        self.lst_stopwords = nltk.corpus.stopwords.words("english")
        self.logger = logging.getLogger("ZSC")
        self.ex = ex
        self.config = read_env_vars()
        self.taxonomy = self.prepare_taxonomy(ex)
        self.logger.info(self.config)
        self.logger.info("********ZSC is initalized***********")

    def read_taxonomy(self, ex: dict):
        ## read the taxonomy from csv
        cs = ex["cs"]
        self.logger.info(self.config[cs])
        df_taxonomy = pd.read_csv(self.config[cs], delimiter=";", keep_default_na=False)
        df_taxonomy_filtered = df_taxonomy.loc[
            df_taxonomy["dimension"] == ex["dimension"]
        ]
        df_taxonomy_filtered.index = range(len(df_taxonomy_filtered))
        return df_taxonomy_filtered

    def preprocess_taxonomy(
        self, taxonomy: pd.DataFrame, cs: str, dimension: str, hierarchy: str
    ):
        ## aggregate name, description and synonyms
        if cs == "CoClass":
            text_col_keys = ["name_eng", "desc_eng", "synonyms_eng"]
            class_desc_index = 8
        elif cs == "SB11":
            text_col_keys = ["name_eng", "desc_eng"]
            class_desc_index = 6
        elif cs == "Tele":
            text_col_keys = ["name_eng", "desc_eng", "synonyms_eng"]
            class_desc_index = 5


        taxonomy["text"] = taxonomy[text_col_keys].fillna("").agg(" ".join, axis=1)
        taxonomy["text_clean"] = taxonomy["text"].apply(
            lambda x: self.utils_preprocess_text(
                x, flg_stemm=False, flg_lemm=True, lst_stopwords=self.lst_stopwords
            )
        )
        ## aggregate nodes

        if hierarchy in ["bottomup", "topdown"]:
            tree = aggregate_nodes(taxonomy, cs, dimension, hierarchy, class_desc_index)
            taxonomy[hierarchy] = taxonomy["identifier"].apply(
                lambda x: tree.get_node(dimension + x).tag
            )
            taxonomy = remove_dummy_nodes(taxonomy, hierarchy)
            taxonomy[hierarchy + "_clean"] = taxonomy[hierarchy].apply(
                lambda x: self.utils_preprocess_text(
                    x, flg_stemm=False, flg_lemm=True, lst_stopwords=self.lst_stopwords
                )
            )
        else:
            taxonomy = remove_dummy_nodes(taxonomy, "text")
        return taxonomy

    def utils_preprocess_text(
        self, text, flg_stemm=False, flg_lemm=True, lst_stopwords=None
    ):
        ## clean (convert to lowercase and remove punctuations and characters and then strip)
        text = re.sub(r"[^\w\s]", "", str(text).lower().strip())

        ## Tokenize (convert from string to list)
        lst_text = text.split()  ## remove Stopwords
        if lst_stopwords is not None:
            lst_text = [word for word in lst_text if word not in lst_stopwords]

        ## Stemming (remove -ing, -ly, ...)
        if flg_stemm == True:
            ps = nltk.stem.porter.PorterStemmer()
            lst_text = [ps.stem(word) for word in lst_text]

        ## Lemmatisation (convert the word into root word)
        if flg_lemm == True:
            lem = nltk.stem.wordnet.WordNetLemmatizer()
            lst_text = [lem.lemmatize(word) for word in lst_text]

        ## back to string from list
        text = " ".join(lst_text)
        return text

    # load sentence model
    def load_sentence_model(self, model_name):
        model = SentenceTransformer(model_name)
        return model

    # create input embedding
    def utils_sentence_bert_embedding(self, txt, nlp):
        X = nlp.encode(txt)
        return X

    def create_embedding(self, df_test_data, df_taxonomy, hierarchy, embedding, model):
        class_key = "text"
        if hierarchy in ["bottomup", "topdown"]:
            class_key = hierarchy

        if embedding == "sentence":
            return self.sentence_embedding(
                model,
                df_test_data["text"],
                df_taxonomy.loc[:, ["identifier", class_key]],
            )

        return None

    def sentence_embedding(self, model, df_test_data, df_taxonomy_aggregated_text):
        # load model
        nlp = self.load_sentence_model(model)

        # input data embedding
        embeddings = [
            self.utils_sentence_bert_embedding(txt, nlp) for txt in df_test_data
        ]
        X = np.array(embeddings)

        # taxonomy embedding
        Y = try_read_taxonomy_embedding(self.ex["cs"], self.ex["dimension"])
        if Y == None:
            Y = {
                row.iloc[0]: self.utils_sentence_bert_embedding(row.iloc[1], nlp)
                for index, row in df_taxonomy_aggregated_text.iterrows()
            }

            save_embedding(Y, self.ex["cs"], self.ex["dimension"])

        return X, Y

    # compute cosine similarities
    def cosine_similarity(self, X, Y):
        similarities = np.array(
            [
                metrics.pairwise.cosine_similarity(X, y.reshape(1, -1)).T.tolist()[0]
                for y in Y.values()
            ]
        ).T
        return similarities

    def get_top_k_label_idx(self, simiArray, k, cutoff):
        # simiArrayAtCutoff = np.array(list(filter(lambda score: score >= cutoff, simiArray)))
        return (-simiArray).argsort()[:k]

    def label_selection(self, Y, similarities, taxonomy, k, cutoff):
        ## adjust and rescal
        labels = list(Y.keys())

        for i in range(len(similarities)):
            ### assign randomly if there is no similarity
            if sum(similarities[i]) == 0:
                similarities[i] = [0] * len(labels)
                similarities[i][np.random.choice(range(len(labels)))] = 1

            ### rescale so their sum = 1
            ##similarities[i] = similarities[i] / sum(similarities[i])

        ## classify the label with highest similarity score
        predicted_prob = similarities

        top_k_predicted_idx = [[""] * k for temp in range(predicted_prob.shape[0])]
        top_k_predicted = [[""] * k for temp in range(predicted_prob.shape[0])]
        top_k_predicted_names = [[""] * k for temp in range(predicted_prob.shape[0])]
        scores = [[""] * k for temp in range(predicted_prob.shape[0])]

        ## get top k labels per requirement
        for i, p in enumerate(predicted_prob):
            top_k_idx = self.get_top_k_label_idx(p, k, cutoff)
            top_k_predicted_idx[i] = top_k_idx
            top_k_predicted[i] = [labels[n] for n in top_k_idx]
            top_k_predicted_names[i] = [
                taxonomy.loc[taxonomy["identifier"] == pred, "name_eng"].item()
                for pred in top_k_predicted[i]
            ]
            scores[i] = [p[n] for n in top_k_predicted_idx[i]]

        return {
            "predicted_labels_idx": top_k_predicted_idx,
            "predicted_labels": top_k_predicted,
            "predicted_labels_names": top_k_predicted_names,
            "scores": scores,
        }

    def global_classifier(self, df_test_data, df_taxonomy, ex):
        hierarchy = ex["hierarchy"]
        model_name = ex["model"]
        embedding = ex["embedding"]
        k = ex["k"]
        cutoff = ex["cutoff"]
        # feature engineering
        df_test_data["text"] = df_test_data["all_text"]
        df_test_data["text_clean"] = df_test_data["all_text_clean"]
        # df_test_data['text'] = df_test_data['req_text']
        # df_test_data['text_clean'] = df_test_data['req_text_clean']

        X, Y = self.create_embedding(
            df_test_data,
            df_taxonomy,
            hierarchy,
            embedding,
            model_name,
        )

        similarities = self.cosine_similarity(X, Y)
        predictions = self.label_selection(Y, similarities, df_taxonomy, k, cutoff)
        return predictions

    def prepare_taxonomy(self, ex):
        tf.keras.backend.clear_session()
        # 2. reading taxonomy
        df_taxonomy_original = self.read_taxonomy(ex)
        df_taxonomy = self.preprocess_taxonomy(
            df_taxonomy_original, ex["cs"], ex["dimension"], ex["hierarchy"]
        )
        return df_taxonomy

    def classify(self, data):
        start_time = time.time()
        # tf.keras.backend.clear_session()
        predictions = self.global_classifier(data, self.taxonomy, self.ex)
        end_time = time.time()
        elapsed_time = "{:.2f}".format(end_time - start_time)

        return predictions, elapsed_time

    def classify_single(self, text):
        requirements = {
            "all_text": [text],
            "all_text_clean": ["-"],
        }
        data = pd.DataFrame(requirements)

        result, time = self.classify(data)

        single_result = {
            "label": result["predicted_labels"][0],
            "desc": result["predicted_labels_names"][0],
            "score": result["scores"][0],
        }

        result_df = pd.DataFrame(single_result)

        return result_df.to_dict("records")
