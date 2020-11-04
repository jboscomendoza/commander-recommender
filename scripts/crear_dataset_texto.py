import json
import re
import string
import numpy as np
import pandas as pd

import gensim
import nltk


with open('commanders.json') as json_file:
    commanders_json = json.load(json_file, encoding="latin-1")


campos = ["id", "name", "oracle_text", "card_faces"]


edh = []


for carta in commanders_json:
    datos = {}
    for field in campos:
        try:
            datos[field] = carta[field]
        except:
            datos[field] = ""
    edh.append(datos)


def get_oracle_text(edh):
    textos = []
    for carta in edh:
        if len(carta["card_faces"]) > 0:
            oracle = []
            for cara in carta["card_faces"]:
                oracle.append(cara["oracle_text"])
            textos.append(" ".join(oracle))
        else:
            textos.append(carta["oracle_text"])
    return textos


mana_cost = "{[0-9WUBRG/PXC]*}"
tap_cost = "{T}"

oracle_text = get_oracle_text(edh)
oracle_text = [re.sub(mana_cost, " mana_cost ", i) for i in oracle_text]
oracle_text = [re.sub(tap_cost, " tap_cost ", i) for i in oracle_text]
oracle_text = [i.lower() for i in oracle_text]
oracle_text = [re.sub('[.,:()"]|(â€”)', " ", i).split() for i in oracle_text]

names = [i["name"] for i in commanders_json]

texto_cartas = dict(zip(names, oracle_text))


# Generar lexico, corpus y tf idf
lexico = gensim.corpora.Dictionary(oracle_text)
corpus = [lexico.doc2bow(i) for i in oracle_text]
tf_idf = gensim.models.TfidfModel(corpus)


# Almacenamiento de similitudes
sims = gensim.similarities.Similarity('text_sim/', tf_idf[corpus], num_features=len(lexico))


# Matrix de similitud
sim_matrix = tf_idf[corpus]

max(sims[sim_matrix][0])


# Lexico e indice manual
lexico = []

for nombre, texto in texto_cartas.items():
    for palabra in texto:
        if palabra not in lexico:
            lexico.append(palabra)

lexico.sort()
len(lexico)

texto_indices = []

for texto in texto_cartas.values():
    indices = []
    for palabra in texto:
        indices.append(lexico.index(palabra))
    texto_indices.append(indices)
