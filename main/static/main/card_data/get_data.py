import requests
import json

# get the default cards from Scryfall
bulk = requests.get('https://api.scryfall.com/bulk-data/oracle-cards')
r = bulk.json()
uri = r.get('download_uri')
card_json = requests.get(uri)
with open('detail_data.json', 'w') as f:
    json.dump(card_json.json(), f)
