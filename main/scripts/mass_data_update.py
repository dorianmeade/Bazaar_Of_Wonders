import requests
import os
import json
import config
import datetime
import pytz
import html
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
# from main.models import Card, Listing

""" remove unless we wind up needing this
# delete the old data files
if os.path.exists("scryfall_bulk_data.json"):
    os.chmod("scryfall_bulk_data.json", 777)
    os.remove("scryfall_bulk_data.json")
if os.path.exists("mtg_json_cards_data.json"):
    os.chmod("mtg_json_cards_data.json", 777)
    os.remove("mtg_json_cards_data.json")"""

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
    except Exception:
        pass  # just get a new token if the above doesn't work for some reason

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
    req = Request(url='https://shop.tcgplayer.com/productcatalog/product/getpricetable?captureFeaturedSellerData=True&'
                      'pageSize=100&productId={0}'.format(product['productId']),
                  headers={'User-Agent': 'Mozilla/5.0', 'Authorization': "Bearer {0}".format(token)})

    # Retrieves the response for the above request in the form of HTML. The try except block is used
    # in case a product ID doesn't exist (which should never happen now, but better to be safe than sorry).
    try:
        page = urlopen(req).read()
    except Exception:
        continue

    # Creates a BeautifulSoup object with the retrieved HTML
    soup = BeautifulSoup(page, 'html.parser')

    product_line = '"product_line": "Magic"'
    product_line_check = str(soup).find(product_line)

    # Finds HTML elements with the desired listing data
    listings = soup.find_all('script', attrs={'type': 'text/javascript'})

    # Checks if there are no listings for a product
    if not listings:
        continue

    listings.pop(0)  # This pop gets rid of some junk data that was captured in the above find_all
    index = 0
    more_listings = True
    product_listings = []

    # Iterates through all the listings for a particular product
    while more_listings:
        try:
            result = listings[index].contents[0].split('\r\n')
            this_listing = {}
            for item in result:
                # the string manipulation of these items assumes standard format where the desired
                # item appears after a colon and is formatted as "<desired item>",
                # html unescape takes care of escape sequences, however, since the content is in a string
                # format it leaves behind the leading \\, so this also assumes that no strings will
                # purposefully have a \\ in them, and removes all instances of \\ from strings
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
                elif item.find('"seller_key":') > 0:
                    this_listing['seller_key'] = html.unescape(item.strip().split(':')[1].strip()[1:-2]).replace('\\', '')
                else:
                    pass
            product_listings.append(this_listing)
            index += 1
        except Exception:
            more_listings = False
    product['listings'] = product_listings

"""
SCRYFALL DATA DOWNLOAD
"""
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

"""
MTGJSON DATA DOWNLOAD
"""
# get the all cards data from MTGJSON
mtg_json_data = requests.request(method="GET", url="https://www.mtgjson.com/files/AllCards.json")
print("Data download end time: {0}".format(datetime.datetime.now()))

# This works like a dictionary
# This iterates through each object in the json file and returns each object's keys and values
# For each key that matches our models, save attribute
# https://stackoverflow.com/questions/18724863/can-i-use-json-data-to-add-new-objects-in-django
"""
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
f.close()
"""