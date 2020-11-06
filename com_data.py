import json

with open('recomendaciones.json') as json_file:
    RECS = json.load(json_file, encoding="utf-8")


NOMBRES = [i["commander"] for i in RECS]


with open('commanders.json') as json_file:
    COMS = json.load(json_file, encoding="utf-8")
