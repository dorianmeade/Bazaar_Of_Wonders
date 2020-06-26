import os
import json


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
            "tcgplayer_id": None,
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
            "card_market_purchase_url": None,
            "tcg_player_purchase_url": None,
            "mtg_stocks_purchase_url": None,
            "quantity": None,
            "condition": None,
            "seller_key": "Seeding Seller",
            "seller_type": "Vendor",
            "sponsored": False,
            "user_listing": False,
            "selling_user_id": 1,
        }
    }

# a dictionary of all the data to save to the db
transfer_to_db = {}

# open the scryfall data and load as json
with open('scryfall_data.json', 'r') as json_file:
    data = json.load(json_file)
    for card in data:
        # going to make each card a dictionary with its oracle id as the key and all the attributes in their
        # own dictionary, this way it can be easily matched to it's corresponding MTGJSON entry by said key and
        # the data from MTG JSON can be added to the value
        if card['oracle_id']:
            id = card['oracle_id']
            transfer_to_db[id] = {}  # initialize empty dictionary to store this cards data
            # add data of interest
            if 'tcgplayer_id' in card.keys():
                transfer_to_db[id]['tcgplayer_id'] = card['tcgplayer_id']
            if 'name' in card.keys():
                transfer_to_db[id]['name'] = card['name']
            if 'image_uris' in card.keys():
                if 'png' in card['image_uris'].keys():
                    transfer_to_db[id]['card_image_loc'] = card['image_uris']['png']
                elif 'normal' in card['image_uris'].keys():
                    transfer_to_db[id]['card_image_loc'] = card['image_uris']['normal']
                elif 'small' in card['image_uris'].keys():
                    transfer_to_db[id]['card_image_loc'] = card['image_uris']['small']
                elif 'large' in card['image_uris'].keys():
                    transfer_to_db[id]['card_image_loc'] = card['image_uris']['large']
            if 'mana_cost' in card.keys():
                transfer_to_db[id]['mana_cost'] = card['mana_cost']
            if 'type_line' in card.keys():
                transfer_to_db[id]['type'] = card['type_line']
            if 'colors' in card.keys():
                transfer_to_db[id]['card_color'] = card['colors']
            if 'keywords' in card.keys():
                transfer_to_db[id]['card_keywords'] = card['keywords']
            if 'set_name' in card.keys():
                transfer_to_db[id]['set_name'] = card['set_name']
            if 'power' in card.keys():
                transfer_to_db[id]['power'] = card['power']
            if 'toughness' in card.keys():
                transfer_to_db[id]['toughness'] = card['toughness']
            if 'collector_number' in card.keys():
                transfer_to_db[id]['collection_number'] = card['collector_number']
            if 'rarity' in card.keys():
                transfer_to_db[id]['rarity'] = card['rarity']
            if 'flavor_text' in card.keys():
                transfer_to_db[id]['flavor_text'] = card['flavor_text']
            if 'artist' in card.keys():
                transfer_to_db[id]['artist'] = card['artist']
            if 'prices' in card.keys():
                if 'usd' in card['prices'].keys():
                    transfer_to_db[id]['price'] = card['prices']['usd']
        # if there is no scryfall oracle id, there is no way to link to mtg json data so skip it
        else:
            continue

# close scryfall data
json_file.close()

# open MTGJSON data and load
f = open('mtg_json_cards_data', 'r')
data = json.load(f)  # this is a dict of the following format:  key='card name', value={<dictionary of card info>}
for key, card in zip(data.keys(), data.values()):
    if card['scryfallOracleId']:
        # if we have a match in the scryfall data
        if card['scryfallOracleId'] in transfer_to_db.keys():
            dict_entry = transfer_to_db[card['scryfallOracleId']]
            # add items special to MTG
            if 'convertedManaCost' in card.keys():
                dict_entry['converted_mana_cost'] = card['convertedManaCost']
            if 'text' in card.keys():
                dict_entry['card_text'] = card['text']
            if 'purchaseUrls' in card.keys():
                if 'cardmarket' in card['purchaseUrls'].keys():
                    dict_entry['card_market_purchase_url'] = card['purchaseUrls']['cardmarket']
                if 'tcgplayer' in card['purchaseUrls'].keys():
                    if 'purchase_urls' not in dict_entry.keys():
                        dict_entry['tcg_player_purchase_url'] = card['purchaseUrls']['tcgplayer']
                if 'mtgstocks' in card['purchaseUrls'].keys():
                    if 'purchase_urls' not in dict_entry.keys():
                        dict_entry['mtg_stocks_purchase_url'] = card['purchaseUrls']['mtgstocks']
            # save MTG JSON uuid in case we want to use that to join with more data later
            if 'uuid' in card.keys():
                dict_entry['mtg_json_uuid'] = card['uuid']

            # fill in any missing data not gotten from scryfall
            if 'name' not in dict_entry.keys() and 'name' in card.keys():
                dict_entry['name'] = card['name']
            if 'mana_cost' not in dict_entry.keys() and 'mana_cost' in card.keys():
                dict_entry['mana_cost'] = card['mana_cost']
            if 'type' not in dict_entry.keys() and 'type' in card.keys():
                dict_entry['type'] = card['type']
            if 'colors' not in dict_entry.keys() and 'colors' in card.keys():
                dict_entry['card_color'] = card['colors']
            if 'power' not in dict_entry.keys() and 'power' in card.keys():
                dict_entry['power'] = card['power']
            if 'toughness' not in dict_entry.keys() and 'toughness' in card.keys():
                dict_entry['toughness'] = card['toughness']
        else:
            # if there is no match already in the dictionary, this is a new card (WONT HAVE PICTURE)
            id = card['scryfallOracleId']
            transfer_to_db[id] = {}  # initialize empty dictionary to store this cards data
            if 'convertedManaCost' in card.keys():
                transfer_to_db[id]['converted_mana_cost'] = card['convertedManaCost']
            if 'text' in card.keys():
                transfer_to_db[id]['card_text'] = card['text']
            if 'purchaseUrls' in card.keys():
                if 'cardmarket' in card['purchaseUrls'].keys():
                    transfer_to_db[id]['card_market_purchase_url'] = card['purchaseUrls']['cardmarket']
                if 'tcgplayer' in card['purchaseUrls'].keys():
                    transfer_to_db[id]['tcg_player_purchase_url'] = card['purchaseUrls']['tcgplayer']
                if 'mtgstocks' in card['purchaseUrls'].keys():
                    transfer_to_db[id]['mtg_stocks_purchase_url'] = card['purchaseUrls']['mtgstocks']
            # save MTG JSON uuid in case we want to use that to join with more data later
            if 'uuid' in card.keys():
                transfer_to_db[id]['mtg_json_uuid'] = card['uuid']
            if 'name' in card.keys():
                transfer_to_db[id]['name'] = card['name']
            if 'mana_cost' in card.keys():
                transfer_to_db[id]['mana_cost'] = card['mana_cost']
            if 'type' in card.keys():
                transfer_to_db[id]['type'] = card['type']
            if 'colors' in card.keys():
                transfer_to_db[id]['card_color'] = card['colors']
            if 'power' in card.keys():
                transfer_to_db[id]['power'] = card['power']
            if 'toughness' in card.keys():
                transfer_to_db[id]['toughness'] = card['toughness']
    # if there is no scryfall id we can't match it to the other data, so skip
    else:
        continue
f.close()

# create json fixtures
rarities, types, cards, listings, rarity_strings, type_strings= [], [], [], [], [], []

# make a generic seller to use for now

for scryfall_id, card_data in zip(transfer_to_db.keys(), transfer_to_db.values()):
    rarity_id = 0
    type_id = 0

    # cannot add without rarity and type FKs
    if 'rarity' not in card_data.keys() or 'type' not in card_data.keys():
        continue
    else:
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
        card["pk"] = scryfall_id
        try:
            if 'tcgplayer_id' in card_data.keys():
                int(card_data['tcgplayer_id'])
                card["fields"]["tcgplayer_id"] = card_data['tcgplayer_id']
            else:
                card["fields"]["tcgplayer_id"] = -1
        except ValueError:
            card["fields"]["tcgplayer_id"] = -1
        card["fields"]["mtg_json_uuid"] = card_data['mtg_json_uuid'] if 'mtg_json_uuid' in card_data.keys() else ""
        card["fields"]["name"] = card_data['name'] if 'name' in card_data.keys() else "Card has no name"
        card["fields"]["card_image_loc"] = card_data['card_image_loc'] \
            if 'card_image_loc' in card_data.keys() else "static/main/images/cards/default.jpg"
        card["fields"]["mana_cost"] = card_data['mana_cost'] if 'mana_cost' in \
                                                                card_data.keys() else "No mana cost available"
        try:
            if 'converted_mana_cost' in card_data.keys():
                int(card_data['converted_mana_cost'])
                card["fields"]["converted_mana_cost"] = card_data['converted_mana_cost']
            else:
                card["fields"]["converted_mana_cost"] = -1
        except ValueError:
            card["fields"]["converted_mana_cost"] = -1
        card["fields"]["type_id"] = type_id
        card["fields"]["card_text"] = card_data['card_text'] if 'card_text' in card_data.keys() \
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
                int(card_data['power'])
                card["fields"]["power"] = card_data['power']
            else:
                card["fields"]["power"] = -1
        except ValueError:
            card["fields"]["power"] = -1
        try:
            if 'toughness' in card_data.keys():
                int(card_data['toughness'])
                card["fields"]["toughness"] = card_data['toughness']
            else:
                card["fields"]["toughness"] = -1
        except ValueError:
            card["fields"]["toughness"] = -1
        try:
            if 'collection_number' in card_data.keys():
                int(card_data['collection_number'])
                card["fields"]["collection_number"] = card_data['collection_number']
            else:
                card["fields"]["collection_number"] = -1
        except ValueError:
            card["fields"]["collection_number"] = -1
        card["fields"]["rarity_id"] = rarity_id
        card["fields"]["flavor_text"] = card_data['flavor_text'] if 'flavor_text' in card_data.keys() \
            else "No flavor text available"
        card["fields"]["artist"] = card_data['artist'] \
            if 'artist' in card_data.keys() else "No artist information available"
        cards.append(card)

        # create listing JSON
        listing = listing_skeleton()
        listing["pk"] = len(listings) + 1
        listing["fields"]["product_id"] = scryfall_id
        listing["fields"]["product_name"] = card_data["name"] if "name" in card_data.keys() else "Card has no name"
        listing["fields"]["set_name"] = card_data['set_name'] if "set_name" in card_data.keys() \
            else "No set name available"
        try:
            if "price" in card_data.keys() and card_data['price'] is not None:
                float(card_data['price'])
                listing["fields"]["price"] = card_data['price']
            else:
                listing["fields"]["price"] = -1
        except ValueError:
            listing["fields"]["price"] = -1
        listing["fields"]["card_market_purchase_url"] = card_data['card_market_purchase_url'] \
            if "card_market_purchase_url" in card_data.keys() else ""
        listing["fields"]["tcg_player_purchase_url"] = card_data['tcg_player_purchase_url'] \
            if "tcg_player_purchase_url" in card_data.keys() else ""
        listing["fields"]["mtg_stocks_purchase_url"] = card_data['mtg_stocks_purchase_url'] \
            if "mtg_stocks_purchase_url" in card_data.keys() else ""
        listing["fields"]["quantity"] = card_data['quantity'] if "quantity" in card_data.keys() else -1
        listing["fields"]["condition"] = card_data['condition'] if "condition" in card_data.keys() \
            else "No condition information available"
        listings.append(listing)
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "fixtures", "{0}"))
with open(basepath.format("rarities.json"), 'w') as f:
    json.dump(rarities, f)
f.close()
with open(basepath.format("types.json"), 'w') as f:
    json.dump(types, f)
f.close()
with open(basepath.format("cards.json"), 'w') as f:
    json.dump(cards, f)
f.close()
with open(basepath.format("listings.json"), 'w') as f:
    json.dump(listings, f)
f.close()

"""
To add these items to the database run this command for each file:
manage.py loaddata <name>.json 
"""
