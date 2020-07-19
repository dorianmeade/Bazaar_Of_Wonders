import requests
import json


# get the all cards data from MTGJSON
def get_data():
    response = requests.request(method="GET", url="https://www.mtgjson.com/files/AllCards.json", )
    with open('main/static/main/card_data/mtg_json_cards_data', 'w') as f:
        json.dump(response.json(), f)
