import json
import re
import string
import gensim
import nltk
import numpy as np
import pandas as pd


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
ids   = [i["id"] for i in commanders_json]


# Generar lexico, corpus y tf idf
lexico = gensim.corpora.Dictionary(oracle_text)
corpus = [lexico.doc2bow(i) for i in oracle_text]
tf_idf = gensim.models.TfidfModel(corpus)


# Almacenamiento de similitudes
sims = gensim.similarities.Similarity('text_sim/', tf_idf[corpus], num_features=len(lexico))


# Matriz de similitud
sim_matrix = tf_idf[corpus]


# Procesamiento para json
def ordenar_sims(sim_orig):
    sims_orden = []
    for i in sims[sim_orig]:
        conjunto = list(tuple(zip(i, names, ids)))
        conjunto = sorted(conjunto, reverse=True)
        sims_orden.append(conjunto[:11])
    return sims_orden


def sims_a_lista(sims_orden):
    lista_recomendaciones = []

    for i in sims_orden:
        salida = {"commander":i[0][1], "id":i[0][2]}
        recomendaciones = []
        for rec in i[1:]:
            valor = rec[0] * 100
            valor = np.round(valor, 2).item()
            item = {"commander":rec[1], "similitud": valor, "id": rec[2]}
            recomendaciones.append(item)
        salida["recomendaciones"] = recomendaciones
        lista_recomendaciones.append(salida)
    
    return lista_recomendaciones


# Exportar recomendaciones
sims_orden = ordenar_sims(sim_matrix)
lista_recom = sims_a_lista(sims_orden)

with open('recomendaciones.json', 'w', encoding='utf-8') as f:
    json.dump(lista_recom, f, ensure_ascii=False, indent=2)


# Lexico e indice manual
texto_cartas = dict(zip(names, oracle_text))

lexico = []

for nombre, texto in texto_cartas.items():
    for palabra in texto:
        if palabra not in lexico:
            lexico.append(palabra)

lexico.sort()
texto_indices = []

for texto in texto_cartas.values():
    indices = []
    for palabra in texto:
        indices.append(lexico.index(palabra))
    texto_indices.append(indices)
