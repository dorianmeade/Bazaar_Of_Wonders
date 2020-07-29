import requests
import os
import sys
import json
import datetime
import pytz
import html
import time
import re
from bs4 import BeautifulSoup, SoupStrainer
from django.conf import settings
from django import setup
sys.path.append("../../../Bazaar_Of_Wonders")
os.environ["DJANGO_SETTINGS_MODULE"] = "bazaar_of_wonders.settings"
setup()
from django.db import connection

# Delete the old data dump files
if os.path.exists("TCG_data.json"):
    os.chmod("TCG_data.json", 777)
    os.remove("TCG_data.json")
if os.path.exists("scryfall_data.json"):
    os.chmod("scryfall_data.json", 777)
    os.remove("scryfall_data.json")
if os.path.exists("MTG_data.json"):
    os.chmod("MTG_data.json", 777)
    os.remove("MTG_data.json")

# While this is done via fixtures, need to delete the old files
if os.path.exists("../fixtures/rarities.json"):
    os.chmod("../fixtures/rarities.json", 777)
    os.remove("../fixtures/rarities.json")
if os.path.exists("../fixtures/types.json"):
    os.chmod("../fixtures/types.json", 777)
    os.remove("../fixtures/types.json")
if os.path.exists("../fixtures/sellers.json"):
    os.chmod("../fixtures/sellers.json", 777)
    os.remove("../fixtures/sellers.json")
if os.path.exists("../fixtures/cards.json"):
    os.chmod("../fixtures/cards.json", 777)
    os.remove("../fixtures/cards.json")
if os.path.exists("../fixtures/listings.json"):
    os.chmod("../fixtures/listings.json", 777)
    os.remove("../fixtures/listings.json")

print("Data download start time: {0}".format(datetime.datetime.now()))
"""
TCG PLAYER DATA DOWNLOAD
"""
# check to see if we have a valid bearer token
token = ""
if os.path.exists('tcg_bearer_token.json'):
    try:
        with open('tcg_bearer_token.json') as json_file:
            token_info = json.load(json_file)
            # only use the token if it is less than 24 hours until it expires, otherwise get a new one
            if (datetime.datetime.now() + datetime.timedelta(hours=24)).astimezone(pytz.utc) < \
                    datetime.datetime.strptime(token_info['.expires'],
                                               "%a, %d %b %Y %H:%M:%S %Z").astimezone(pytz.utc):
                token = token_info['access_token']
        json_file.close()
    except Exception:
        pass  # just get a new token if the above doesn't work for some reason

if not token:
    if os.path.exists('tcg_bearer_token.json'):
        os.chmod("tcg_bearer_token.json", 777)
        os.remove("tcg_bearer_token.json")

    response = requests.request(method="POST", url="https://api.tcgplayer.com/token",
                                headers={'accept': '*/*', 'Content-Type': 'text/plain'},
                                data="grant_type=client_credentials&client_id={0}&client_secret={1}".
                                format(settings.TCGPLAYER_PUBLIC_KEY, settings.TCGPLAYER_PRIVATE_KEY))
    token = json.loads(response.text)["access_token"]
    # save token for later use
    with open('tcg_bearer_token.json', 'w') as f:
        json.dump(response.json(), f)
    f.close()

# get mtg catalog id, probably will forever be 1, but jic
mtg_cat_id, categories, last_total = -1, [], 100
# no need to loop again if the last total wasn't 100 b/c we're at the end of the list
while mtg_cat_id < 0 and last_total == 100 and len(categories) < 10000:
    response = json.loads(requests.request(method="GET", url="https://api.tcgplayer.com/catalog/categories?limit=100&"
                                                             "offset={0}&sortOrder=categoryId".format(len(categories)),
                                           headers={'accept': 'application/json', 'Content-Type': 'text/plain',
                                                    'Authorization': "Bearer {0}".format(token)}).text)['results']
    categories.extend(response)
    last_total = len(response)
    for category in categories:
        if category['name'] == 'Magic':
            mtg_cat_id = category['categoryId']
            break

# get info about all the mtg cards
last_total, tcg_data = 100, []
while len(tcg_data) < 1000000 and last_total == 100:
    response = json.loads(requests.request(method="GET", url="https://api.tcgplayer.com/catalog/products?limit=100&"
                                                             "offset={0}&categoryId={1}&getExtendedFields=True".
                                           format(len(tcg_data), mtg_cat_id),
                                           headers={'accept': 'application/json', 'Content-Type': 'text/plain',
                                                    'Authorization': "Bearer {0}".format(token)}).text)['results']
    tcg_data.extend(response)
    last_total = len(response)

# use scraper to get vendor information
for product in tcg_data:
    # maxes out at 100 listings, but honestly that seems like plenty so leaving it
    try:
        response = requests.get(url='https://shop.tcgplayer.com/productcatalog/product/getpricetable?'
                                    'captureFeaturedSellerData=True&pageSize=100&productId={0}'.
                                format(product['productId']),
                                headers={'User-Agent': 'Mozilla/5.0', 'Authorization': "Bearer {0}".format(token)}).text
    except Exception:
        # wait a few seconds and try again, if it fails again, skip it
        time.sleep(5)
        try:
            response = requests.get(url='https://shop.tcgplayer.com/productcatalog/product/getpricetable?'
                                        'captureFeaturedSellerData=True&pageSize=100&productId={0}'.
                                    format(product['productId']),
                                    headers={'User-Agent': 'Mozilla/5.0',
                                             'Authorization': "Bearer {0}".format(token)}).text
        except Exception:
            continue
    # Creates a BeautifulSoup object with the retrieved HTML, then does find to get result set
    listings = BeautifulSoup(response, 'html.parser',
                             parse_only=SoupStrainer("script", attrs={'type': 'text/javascript'})).find_all("script")

    if listings:
        product_listings = []
        listings.pop(0)
        for listing in listings:
            try:
                result = listing.contents[0].split('\r\n')
                this_listing = {}
                # the string manipulation of these items assumes standard format where the desired item appears after a colon
                # and is formatted as "<desired item>", html unescape takes care of escape sequences, however since the
                # content is in a string format it leaves behind the leading \\, so this also assumes that no strings will
                # purposefully have a \\ in them, and removes all instances of \\ from strings
                for item in result:
                    if item.find('"set_name":') > 0:
                        this_listing['set_name'] = html.unescape(item.strip().split(':')[1].strip()[1:-2]).replace('\\', '')
                    elif item.find('"price":') > 0:
                        this_listing['price'] = float(item.strip().split(':')[1].strip()[1:-2])
                    elif item.find('"quantity":') > 0:
                        # only do if a quantity is available
                        if item.strip().split(':')[1].strip()[1:-2]:
                            this_listing['quantity'] = int(item.strip().split(':')[1].strip()[1:-2])
                    elif item.find('"condition":') > 0:
                        this_listing['condition'] = html.unescape(item.strip().split(':')[1].strip()[1:-2]).replace('\\', '')
                    elif item.find('"seller":') > 0:
                        this_listing['seller_name'] = html.unescape(item.strip().split(':')[1].strip()[1:-2]).replace('\\', '')
                    else:
                        pass
                product_listings.append(this_listing)
            except Exception:
                continue  # if there are no contents in the listing, skip it
        product['listings'] = product_listings

print("TCG Data grab ended: {0}".format(datetime.datetime.now()))
# data dump in case parsing breaks somewhere (won't have to pull again)
with open('TCG_data.json', 'w') as f:
    json.dump(tcg_data, f)
f.close()

"""
To use if parsing data from saved files
with open('TCG_data.json') as json_file:
    tcg_data = json.load(json_file)
json_file.close()
"""

"""
SCRYFALL DATA DOWNLOAD
"""

# for debugging purposes only, loading up from old file
# scryfall_data = json.load(open('scryfall_data.json', 'r'))

# this gets the most recent download uri for the most recent data
response = requests.request(method="GET", url="https://api.scryfall.com/bulk-data", )

# this finds the oracle cards download uri, makes the get request and saves the data
scryfall_data = []
for object in json.loads(response.text)['data']:
    if object['type'] == 'oracle_cards':
        scryfall_data = json.loads(requests.request(method="GET", url="{0}".format(object['download_uri'])).text)
        break
    else:
        continue
print("Scryfall data grab ended: {0}".format(datetime.datetime.now()))
# data dump in case parsing breaks somewhere (won't have to pull again)
with open('scryfall_data.json', 'w') as f:
    json.dump(scryfall_data, f)
f.close()

"""
To use if parsing data from saved files
with open('scryfall_data.json') as json_file:
    scryfall_data = json.load(json_file)
json_file.close()
"""

"""
MTGJSON DATA DOWNLOAD
"""
# for debugging purposes only, loading up from old file
# mtg_json_data = json.load(open('mtg_json_cards_data', 'r'))

# get the all cards data from MTGJSON
mtg_json_data = json.loads(requests.request(method="GET", url="https://www.mtgjson.com/files/AllCards.json").text)
print("Data download end time: {0}".format(datetime.datetime.now()))
# data dump in case parsing breaks somewhere (won't have to pull again)
with open('MTG_data.json', 'w') as f:
    json.dump(mtg_json_data, f)
f.close()

"""
To use if parsing data from saved files
with open('MTG_data.json') as json_file:
    mtg_json_data = json.load(json_file)
json_file.close()
"""

"""
Parse through each data set and construct dictionaries for each record that align with our models
"""


def rarity_skeleton():
    return {
        "model": "main.Card_Rarity",
        "pk": None,
        "fields": {
            "card_rarity": None
        }
    }


def type_skeleton():
    return {
        "model": "main.Card_Type",
        "pk": None,
        "fields": {
            "card_type": None
        }
    }


def card_skeleton():
    return {
        "model": "main.Card",
        "pk": None,
        "fields": {
            "scryfall_id": None,
            "mtg_json_uuid": None,
            "name": None,
            "card_image_loc": None,
            "mana_cost": None,
            "converted_mana_cost": None,
            "type_id": None,
            "card_text": None,
            "card_color": None,
            "card_keywords": None,
            "set_name": None,
            "power": None,
            "toughness": None,
            "collection_number": None,
            "rarity_id": None,
            "flavor_text": None,
            "artist": None,
            "card_market_purchase_url": None,
            "tcg_player_purchase_url": None,
            "mtg_stocks_purchase_url": None,
            "last_updated": None
        }
    }


def seller_skeleton():
    return{
        "model": "main.Seller",
        "pk": None,
        "fields": {
            "seller_user": None,
            "seller_name": None,
            "seller_type": "Imported",
            "location": None,
            "completed_sales": 0
        }
    }


def listing_skeleton():
    return {
        "model": "main.Listing",
        "pk": None,
        "fields": {
            "product_id": None,
            "product_name": None,
            "product_line": "Magic The Gathering",
            "set_name": None,
            "price": None,
            "quantity": None,
            "condition": None,
            "seller_key": None,
            "sponsored": False,
            "user_listing": False,
            "last_updated": None,
        }
    }


# get the MTG rarities
rarities = json.loads(requests.request(method="GET", url="https://api.tcgplayer.com/catalog/categories/{0}/rarities".
                                       format(mtg_cat_id),
                                       headers={'accept': 'application/json', 'Content-Type': 'text/plain',
                                                'Authorization': "Bearer {0}".format(token)}).text)['results']
tcg_rarities = {}
for rarity in rarities:
    tcg_rarities[rarity['dbValue']] = rarity['displayText']

# a dictionary of all the data to save to the db
transfer_to_db = {}

# breakdown tcg player data
for item in tcg_data:
    if 'productId' in item.keys():
        id = item['productId']
        transfer_to_db[id] = {}
        if 'name' in item.keys():
            transfer_to_db[id]['name'] = item['name']
        if 'imageUrl' in item.keys():
            transfer_to_db[id]['card_image_loc'] = item['imageUrl']
        if 'url' in item.keys():
            transfer_to_db[id]['tcg_player_purchase_url'] = item['url']
        if 'extendedData' in item.keys():
            for extended_item in item['extendedData']:
                if 'name' in extended_item.keys():
                    if extended_item['name'] == 'Rarity':
                        transfer_to_db[id]['rarity'] = tcg_rarities[extended_item['value']]
                    elif extended_item['name'] == 'Subtype':
                        transfer_to_db[id]['type'] = extended_item['value']
                    elif extended_item['name'] == 'P':
                        transfer_to_db[id]['power'] = extended_item['value']
                    elif extended_item['name'] == 'T':
                        transfer_to_db[id]['toughness'] = extended_item['value']
                    elif extended_item['name'] == 'OracleText':
                        transfer_to_db[id]['card_text'] = extended_item['value']
        if 'listings' in item.keys():
            if 'set_name' in item['listings'][0].keys():
                transfer_to_db[id]['set_name'] = item['listings'][0]['set_name']  # assume only one set per card
            transfer_to_db[id]['listings'] = item['listings']
    else:
        continue

match_tcg_to_scryfall = {}
for item in scryfall_data:
    if 'tcgplayer_id' in item.keys():
        # if we have a match in the TCG data
        if item['tcgplayer_id'] in transfer_to_db.keys():
            dict_entry = transfer_to_db[item['tcgplayer_id']]
            # add data specific to Scryfall
            if 'oracle_id' in item.keys():
                dict_entry['scryfall_id'] = item['oracle_id']
                # make a dict that matches oracle ids to TCGPlayer ids b/c MTGJSON only has oracle
                match_tcg_to_scryfall[item['oracle_id']] = item['tcgplayer_id']
            if 'mana_cost' in item.keys():
                dict_entry['mana_cost'] = item['mana_cost']
            if 'cmc' in item.keys():
                dict_entry['converted_mana_cost'] = item['cmc']
            if 'colors' in item.keys():
                dict_entry['card_color'] = item['colors']
            if 'keywords' in item.keys():
                dict_entry['card_keywords'] = item['keywords']
            if 'collector_number' in item.keys():
                dict_entry['collection_number'] = item['collector_number']
            if 'artist' in item.keys():
                dict_entry['artist'] = item['artist']
            if 'purchase_uris' in item.keys():
                if 'tcg_player_purchase_url' not in dict_entry.keys() and 'tcg_player_purchase_url' in item['purchaseUrls'].keys():
                    dict_entry['tcg_player_purchase_url'] = item['purchaseUrls']['tcgplayer']
                if 'cardmarket' in item['purchaseUrls'].keys():
                    dict_entry['card_market_purchase_url'] = item['purchaseUrls']['cardmarket']
                if 'mtgstocks' in item['purchaseUrls'].keys():
                    dict_entry['mtg_stocks_purchase_url'] = item['purchaseUrls']['mtgstocks']
            # add things that should have come from TCG if they are missing
            if 'name' not in dict_entry.keys() and 'name' in item.keys():
                dict_entry['name'] = item['name']
            if 'card_image_loc' not in dict_entry.keys() and 'image_uris' in item.keys():
                if 'png' in item['image_uris'].keys():
                    dict_entry['card_image_loc'] = item['image_uris']['png']
                elif 'normal' in item['image_uris'].keys():
                    dict_entry['card_image_loc'] = item['image_uris']['normal']
                elif 'small' in item['image_uris'].keys():
                    dict_entry['card_image_loc'] = item['image_uris']['small']
                elif 'large' in item['image_uris'].keys():
                    dict_entry['card_image_loc'] = item['image_uris']['large']
            if 'flavor_text' not in dict_entry.keys() and 'flavor_text' in item.keys():
                dict_entry['flavor_text'] = item['flavor_text']
            if 'type' not in dict_entry.keys() and 'type_line' in item.keys():
                dict_entry['type'] = item['type_line']
            if 'card_text' not in dict_entry.keys() and 'oracle_text' in item.keys():
                dict_entry['card_text'] = item['oracle_text']
            if 'power' not in dict_entry.keys() and 'power' in item.keys():
                dict_entry['power'] = item['power']
            if 'toughness' not in dict_entry.keys() and 'toughness' in item.keys():
                dict_entry['toughness'] = item['toughness']
            if 'set_name' not in dict_entry.keys() and 'set_name' in item.keys():
                dict_entry['set_name'] = item['set_name']
            if 'rarity' not in dict_entry.keys() and 'rarity' in item.keys():
                dict_entry['rarity'] = item['rarity']
    # if there is no tcgplayer id, there is no way to link to TCG Player data so just skip it
    else:
        continue

for key in mtg_json_data.keys():
    item = mtg_json_data[key]
    if 'scryfallOracleId' in item.keys():
        # if we have a match in the scryfall data
        if item['scryfallOracleId'] in match_tcg_to_scryfall.keys():
            dict_entry = transfer_to_db[match_tcg_to_scryfall[item['scryfallOracleId']]]
            # add items special to MTG
            if 'purchaseUrls' in item.keys():
                if 'card_market_purchase_url' not in dict_entry.keys() and 'cardmarket' in item['purchaseUrls'].keys():
                    dict_entry['card_market_purchase_url'] = item['purchaseUrls']['cardmarket']
                if 'tcg_player_purchase_url' not in dict_entry.keys() and 'tcgplayer' in item['purchaseUrls'].keys():
                    dict_entry['tcg_player_purchase_url'] = item['purchaseUrls']['tcgplayer']
                if 'mtg_stocks_purchase_url' not in dict_entry.keys() and 'mtgstocks' in item['purchaseUrls'].keys():
                    dict_entry['mtg_stocks_purchase_url'] = item['purchaseUrls']['mtgstocks']
            # save MTG JSON uuid in case we want to use that to join with more data later
            if 'uuid' in item.keys():
                dict_entry['mtg_json_uuid'] = item['uuid']
            # fill in any missing data not gotten from scryfall
            if 'converted_mana_cost' not in dict_entry.keys() and 'convertedManaCost' in item.keys():
                dict_entry['converted_mana_cost'] = item['convertedManaCost']
            if 'card_text' not in dict_entry.keys() and 'text' in item.keys():
                dict_entry['card_text'] = item['text']
            if 'name' not in dict_entry.keys() and 'name' in item.keys():
                dict_entry['name'] = item['name']
            if 'mana_cost' not in dict_entry.keys() and 'mana_cost' in item.keys():
                dict_entry['mana_cost'] = item['mana_cost']
            if 'type' not in dict_entry.keys() and 'type' in item.keys():
                dict_entry['type'] = item['type']
            if 'colors' not in dict_entry.keys() and 'colors' in item.keys():
                dict_entry['card_color'] = item['colors']
            if 'power' not in dict_entry.keys() and 'power' in item.keys():
                dict_entry['power'] = item['power']
            if 'toughness' not in dict_entry.keys() and 'toughness' in item.keys():
                dict_entry['toughness'] = item['toughness']
    else:
        continue

rarities, types, sellers, cards, listings, rarity_strings, type_strings, seller_strings = [], [], [], [], [], [], [], []
no_html = re.compile('<.*?>')

for tcgplayer_id, card_data in zip(transfer_to_db.keys(), transfer_to_db.values()):
    rarity_id, type_id, seller_id = 0, 0, 0

    # cannot add without rarity and type FKs
    if 'rarity' not in card_data.keys():
        card_data['rarity'] = 'Unknown Rarity'
    if 'type' not in card_data.keys():
        card_data['type'] = 'Unknown Type'
    # check to see if rarity and type already added, if so get pk, if not add them
    if card_data['rarity'] in rarity_strings:
        rarity_id = rarity_strings.index(card_data['rarity']) + 1
    else:
        rarity = rarity_skeleton()
        rarity_id = len(rarity_strings) + 1
        rarity["pk"] = rarity_id
        rarity["fields"]["card_rarity"] = card_data['rarity']
        rarity_strings.append(card_data['rarity'])
        rarities.append(rarity)
    if card_data['type'] in type_strings:
        type_id = type_strings.index(card_data['type']) + 1
    else:
        type = type_skeleton()
        type_id = len(type_strings) + 1
        type["pk"] = type_id
        type["fields"]["card_type"] = card_data['type']
        type_strings.append(card_data['type'])
        types.append(type)

    # create the card JSON
    card = card_skeleton()
    card["pk"] = tcgplayer_id
    card["fields"]["scryfall_id"] = card_data['scryfall_id'] if 'scryfall_id' in card_data.keys() else ""
    card["fields"]["mtg_json_uuid"] = card_data['mtg_json_uuid'] if 'mtg_json_uuid' in card_data.keys() else ""
    card["fields"]["name"] = card_data['name'] if 'name' in card_data.keys() else "Card has no name"
    card["fields"]["card_image_loc"] = card_data['card_image_loc'] \
        if 'card_image_loc' in card_data.keys() else "static/main/images/cards/default.jpg"
    card["fields"]["mana_cost"] = card_data['mana_cost'] if 'mana_cost' in \
                                                            card_data.keys() else "No mana cost available"
    try:
        if 'converted_mana_cost' in card_data.keys():
            card["fields"]["converted_mana_cost"] = int(card_data['converted_mana_cost'])
        else:
            card["fields"]["converted_mana_cost"] = -1
    except ValueError:
        card["fields"]["converted_mana_cost"] = -1
    card["fields"]["type_id"] = type_id
    card["fields"]["card_text"] = re.sub(no_html, '', card_data['card_text']) if 'card_text' in card_data.keys() \
        else "No text available"
    color = ""
    if 'card_color' in card_data.keys():
        for color in card_data['card_color']:
            color += "{0}, ".format(color)
    card["fields"]["card_color"] = color[:-2] if color != "" \
        else "No color available"  # remove last comma and space
    keyword = ""
    if 'card_keywords' in card_data.keys():
        for keyword in card_data['card_keywords']:
            color += "{0}, ".format(keyword)
    card["fields"]["card_keywords"] = keyword[:-2] if keyword != "" \
        else "No keywords available"  # remove last comma and space
    card["fields"]["set_name"] = card_data['set_name'] if 'set_name' in card_data.keys() \
        else "No set name available"
    try:
        if 'power' in card_data.keys():
            card["fields"]["power"] = int(card_data['power'])
        else:
            card["fields"]["power"] = -1
    except ValueError:
        card["fields"]["power"] = -1
    try:
        if 'toughness' in card_data.keys():
            card["fields"]["toughness"] = int(card_data['toughness'])
        else:
            card["fields"]["toughness"] = -1
    except ValueError:
        card["fields"]["toughness"] = -1
    try:
        if 'collection_number' in card_data.keys():
            card["fields"]["collection_number"] = int(card_data['collection_number'])
        else:
            card["fields"]["collection_number"] = -1
    except ValueError:
        card["fields"]["collection_number"] = -1
    card["fields"]["rarity_id"] = rarity_id
    card["fields"]["flavor_text"] = re.sub(no_html, '', card_data['flavor_text']) if 'flavor_text' in card_data.keys() \
        else "No flavor text available"
    card["fields"]["artist"] = card_data['artist'] \
        if 'artist' in card_data.keys() else "No artist information available"
    card["fields"]["card_market_purchase_url"] = card_data['card_market_purchase_url'] \
        if "card_market_purchase_url" in card_data.keys() else ""
    card["fields"]["tcg_player_purchase_url"] = card_data['tcg_player_purchase_url'] \
        if "tcg_player_purchase_url" in card_data.keys() else ""
    card["fields"]["mtg_stocks_purchase_url"] = card_data['mtg_stocks_purchase_url'] \
        if "mtg_stocks_purchase_url" in card_data.keys() else ""
    card['fields']['last_updated'] = datetime.datetime.isoformat(datetime.datetime.now())
    cards.append(card)

    # create listing JSON
    if 'listings' in card_data.keys():
        for listing_data in card_data['listings']:
            # make sure we have the seller set up and there is a price
            if 'seller_name' not in listing_data.keys() or \
                    ('price' in listing_data.keys() and listing_data['price'] == ''):
                continue
            else:
                if listing_data['seller_name'] in seller_strings:
                    seller_id = seller_strings.index(listing_data['seller_name']) + 1
                else:
                    seller = seller_skeleton()
                    seller_id = len(seller_strings) + 1
                    seller["pk"] = seller_id
                    seller["fields"]["seller_name"] = listing_data['seller_name']
                    seller_strings.append(listing_data['seller_name'])
                    sellers.append(seller)
            listing = listing_skeleton()
            listing["pk"] = len(listings) + 1
            listing["fields"]["product_id"] = tcgplayer_id
            listing["fields"]["product_name"] = card_data["name"] if "name" in card_data.keys() else "Card has no name"
            listing["fields"]["set_name"] = listing_data['set_name'] if "set_name" in listing_data.keys() \
                else "No set name available"
            try:
                if "price" in listing_data.keys() and listing_data['price'] is not None:
                    listing["fields"]["price"] = float(listing_data['price'])
                else:
                    listing["fields"]["price"] = -1
            except ValueError:
                listing["fields"]["price"] = -1
            listing["fields"]["quantity"] = listing_data['quantity'] if "quantity" in listing_data.keys() else -1
            listing["fields"]["condition"] = listing_data['condition'] if "condition" in listing_data.keys() \
                else "No condition information available"
            listing['fields']['seller_key'] = seller_id
            listing['fields']['last_updated'] = datetime.datetime.isoformat(datetime.datetime.now())
            listings.append(listing)

if not os.path.exists("../fixtures"):
    os.mkdir("../fixtures")
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "", "../fixtures", "{0}"))
with open(basepath.format("rarities.json"), 'w') as f:
    json.dump(rarities, f)
f.close()
with open(basepath.format("types.json"), 'w') as f:
    json.dump(types, f)
f.close()
with open(basepath.format("sellers.json"), 'w') as f:
    json.dump(sellers, f)
f.close()
with open(basepath.format("cards.json"), 'w') as f:
    json.dump(cards, f)
f.close()
with open(basepath.format("listings.json"), 'w') as f:
    json.dump(listings, f)
f.close()

with connection.cursor() as cursor:
    cursor.execute("BEGIN")
    cursor.execute("DELETE FROM main_listing")
    cursor.execute("DELETE FROM main_seller")
    cursor.execute("DELETE FROM main_card")
    cursor.execute("DELETE FROM main_card_type")
    cursor.execute("DELETE FROM main_card_rarity")
    cursor.execute("COMMIT")

"""
For now to update the db run the commands below.
manage.py loaddata rarities.json 
manage.py loaddata types.json 
manage.py loaddata sellers.json 
manage.py loaddata cards.json 
manage.py loaddata listings.json 
"""
