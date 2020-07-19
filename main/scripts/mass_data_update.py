import requests
import os
import json
import config
import datetime
import pytz

# delete the old data files
if os.path.exists("scryfall_bulk_data.json"):
    os.chmod("scryfall_bulk_data.json", 777)
    os.remove("scryfall_bulk_data.json")
if os.path.exists("mtg_json_cards_data.json"):
    os.chmod("mtg_json_cards_data.json", 777)
    os.remove("mtg_json_cards_data.json")

# check to see if we have a valid bearer token
token = ""
if os.path.exists('tcg_bearer_token.json'):
    with open('tcg_bearer_token.json') as json_file:
        token_info = json.load(json_file)
        # only use the token if it is less than 24 hours until it expires, otherwise get a new one
        if (datetime.datetime.now() + datetime.timedelta(hours=3)).astimezone(pytz.utc) < \
                datetime.datetime.strptime(token_info['.expires'], "%a, %d %b %Y %H:%M:%S %Z" ).astimezone(pytz.utc):
            token = token_info['access_token']

if not token:
    if os.path.exists('tcg_bearer_token.json'):
        os.chmod("tcg_bearer_token.json", 777)
        os.remove("tcg_bearer_token.json")

    response = requests.request(method="POST", url="https://api.tcgplayer.com/token",
                                headers={'accept': '*/*', 'Content-Type': 'text/plain'},
                                data="grant_type=client_credentials&client_id={0}&client_secret={1}".
                                format(config.TCGPlayer_public_key, config.TCGPlayer_private_key))
    token = json.loads(response.text)["access_token"]
    # save token for later use
    with open('tcg_bearer_token.json', 'w') as f:
        json.dump(response.json(), f)
        f.close()

# get data from TCG player
# TODO, this is not done (semi-obviously, haha)
all_products = requests.request(method="GET", url="https://api.tcgplayer.com/catalog/products",
                                headers={'accept': '*/*', 'Content-Type': 'text/plain',
                                         'Authorization': "Bearer {0}".format(token)},
                                data="limit=10000000000") # limit not working yet

# get the bulk data from scryfall, note this takes ten thousand years (i.e. like 5 minutes) to download
response = requests.request(method="GET", url="https://api.scryfall.com/bulk-data", )

for object in json.loads(response.text)['data']:
    if object['type'] == 'oracle_cards':
        response = requests.request(method="GET", url="{0}".format(object['download_uri']), )
        with open('scryfall_bulk_data.json', 'w') as f:
            json.dump(response.json(), f)
        f.close()
        break
    else:
        continue

# get the all cards data from MTGJSON
response = requests.request(method="GET", url="https://www.mtgjson.com/files/AllCards.json", )
with open('mtg_json_cards_data.json', 'w') as f:
    json.dump(response.json(), f)
    f.close()
