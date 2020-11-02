import json
import re
import pandas as pd
import numpy as np

with open('commanders.json') as json_file:
    commanders_json = json.load(json_file, encoding="utf-8")

campos = [
    "id", "name", "mana_cost", "cmc", "power", "toughness", "colors", "color_identity", 
    "keywords", "type_line", "oracle_text"
]

edh = []

for carta in commanders_json:
    datos = {}
    for field in campos:
        try:
            datos[field] = carta[field]
        except:
            datos[field] = []
    edh.append(datos)

commanders = pd.DataFrame(edh)

# Transformacion 
def transformar(entrada, referencia, valor_vacio):
    transformacion = []
    for contenido in entrada:
        salida = []
        if contenido == []:
            contenido = [valor_vacio]
        for i in referencia:
            if i in contenido:
                salida.append(1)
            else:
                salida.append(0)
        transformacion.append(salida)
    return pd.DataFrame(transformacion, columns=referencia)


# Recodificar colores
colors = ["W", "U", "B", "R", "G", "C"]
df_colors = transformar(commanders["colors"], colors, "C")

# Recodificar identidad de color
df_identidad = transformar(commanders["color_identity"], colors, "C")
df_identidad.columns = ["Identidad {}".format(i) for i in colors]

# Recodificar keywords
keywords = list(commanders["keywords"])
keywords = [item for sublist in keywords for item in sublist]
keywords = sorted(set(keywords))
df_keywords = transformar(commanders["keywords"], keywords, "None")

# Recodificar tipo de carta
linea_tipo = [i.replace(' â€” ', "_") for i in commanders["type_line"]]

tipos = [re.sub("Legendary |_.*", "", i).split(" ") for i in linea_tipo]
tipos_unicos = [item for sublist in tipos for item in sublist]
tipos_unicos = sorted(set(tipos_unicos))
df_tipos = transformar(tipos, tipos_unicos, "NoType")

# Recodificar subtipos de carta
subtipos = [re.sub(".*_|/.*", "", i).split(" ") for i in linea_tipo]
subtipos_unicos = [item for sublist in subtipos for item in sublist]
subtipos_unicos = sorted(set(subtipos_unicos))
df_subtipos = transformar(subtipos, subtipos_unicos, "NoSubtype")

# Dataset rasgos
rasgos = pd.concat([df_colors, df_identidad, df_keywords, df_tipos, df_subtipos], axis=1)

rasgos.to_csv("rasgos.csv")
