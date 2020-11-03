import json
import re
import string
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


mana_cost = "{[1-9WUBRG/P]*}"
tap_cost = "{T}"

oracle_text = get_oracle_text(edh)
oracle_text = [re.sub(mana_cost, "mana_cost ", i) for i in oracle_text]
oracle_text = [re.sub(tap_cost, "tap_cost ", i) for i in oracle_text]
oracle_text = [i.lower() for i in oracle_text]
oracle_text = [re.sub("[.,:()]|(â€”)", " ", i).split() for i in oracle_text]

names = [i["name"] for i in commanders_json]


texto_cartas = pd.DataFrame(list(zip(names, oracle_text)), columns=["name", "oracle_text"])
