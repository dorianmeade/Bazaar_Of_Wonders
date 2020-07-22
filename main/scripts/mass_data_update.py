import requests
import os
import json
#import config
import datetime
import pytz
from main.models import Card, Listing

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


# This works like a dictionary
# This iterates through each object in the json file and returns each object's keys and values
# For each key that matches our models, save attribute
# https://stackoverflow.com/questions/18724863/can-i-use-json-data-to-add-new-objects-in-django

with open('scryfall_bulk_data.json', 'r') as json_file:
    data = json.load(json_file)
    for item in data:
        c = Card()
        l = Listing()

        for k, v in iter(item.items()):
            # for Card model
            if k == 'oracle_id':
                setattr(c, 'product_id', v)
            if k == 'name':
                setattr(c, 'name', v)
                setattr(l, 'product_name', v)
            if k == 'image_uris':
                for g, h in iter(k.items()):
                    if g == 'normal':
                        setattr(c, 'card_image_loc', h)
            if k == 'cmc':
                setattr(c, 'converted_mana_cost', v)
            if k == 'type_line':
                setattr(c, 'type_id', v)
            if k == 'oracle_text':
                setattr(c, 'card_text', v)
            if k == 'colors':
                setattr(c, 'card_color', v)
            if k == 'keywords':
                setattr(c, 'card_keywords', v)
            if k == 'collector_number':
                setattr(c, 'collection_number', v)
            if k == 'rarity':
                setattr(c, 'rarity_id', v)
            if k == 'set_name':
                setattr(c, 'set_name', v)
                setattr(l, 'set_name', v)
            
            # for Listing Model
            if k == 'prices':
                for g, h in iter(k.items()):
                    if g == 'usd':
                        setattr(l, 'price', h)
            if k == 'purchase_uris':
                for g, h in iter(k.items()):
                    if g == 'tcgplayer':
                        setattr(l, 'tcg_player_purchase_url', h)
                    if g == 'cardmarket':
                        setattr(l, 'card_market_purchase_url', h)
        # Save to db
        c.save()
        l.save()