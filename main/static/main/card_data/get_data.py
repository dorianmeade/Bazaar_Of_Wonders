import requests
import json

# get the all cards data from MTGJSON
response = requests.request(method="GET", url="https://www.mtgjson.com/files/AllCards.json", )
with open('mtg_json_cards_data', 'w') as f:
    json.dump(response.json(), f)
