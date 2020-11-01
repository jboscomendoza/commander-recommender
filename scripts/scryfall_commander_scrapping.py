import json
import pandas as pd
import requests


search_commanders = "https://api.scryfall.com/cards/search?q=is%3Acommander"
response_commanders = requests.get(search_commanders)
json_commanders = response_commanders.json()


commanders = []
commanders.append(json_commanders["data"])


next_page = json_commanders["next_page"]
has_more = json_commanders["has_more"]


while has_more:
    print(next_page)
    response_next = requests.get(next_page)
    json_next = response_next.json()
    commanders.append(json_next["data"])
    if json_next["has_more"] :
        next_page = json_next["next_page"]
    has_more = json_next["has_more"]


commanders = [item for sublist in commanders for item in sublist]


with open('commanders.json', 'w', encoding='utf-8') as f:
    json.dump(commanders, f, ensure_ascii=False, indent=4)
