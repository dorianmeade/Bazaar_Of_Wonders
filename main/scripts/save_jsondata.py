"""
import sqlite3
import json
import yaml
from main.models import Card, Card_Rarity, Card_Type

conn = sqlite3.connect('bazaar.db')
c = conn.cursor()

def run():
    card_objects = {}
    card_objects = data_to_dict()
    for card in card_objects:
        c.execute("INSERT INTO Card VALUES(card, tcg_id, name, card_image_loc, mana_cost, cmc, card_text, card_color, card_keywords, set_name, power, toughness, collection_number, flavor_text, artist, prices)", [card, card_objects[card][*tcg_id], card_objects[card][*name], card_objects[card][*card_image_loc], card_objects[card][*mana_cost], card_objects[card][*cmc], card_objects[card][*card_text], card_objects[card][*card_color], card_objects[card][*card_keywords], card_objects[card][*set_name], card_objects[card][*power], card_objects[card][*toughness], card_objects[card][*collection_number], card_objects[card][*flavor_text], card_objects[card][*artist], card_objects[card][*prices]])
    conn.commit()
    c.close()
    conn.close()
    
def data_to_dict():
    # a dictionary of all the data to save to the db
    transfer_to_db = {}

    ROOT_FILE = 'main/static/main/card_data/scryfall_data.json'

    #Card = apps.get_model('main', 'Card')
    with open(ROOT_FILE, 'r', encoding='utf8') as json_file:
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
                    transfer_to_db[id]['*tcg_id'] = card['tcgplayer_id']
                if 'name' in card.keys():
                    transfer_to_db[id]['*name'] = card['name']
                if 'image_uris' in card.keys():
                    if 'png' in card['image_uris'].keys():
                        transfer_to_db[id]['*card_image_loc'] = card['image_uris']['png']
                if 'mana_cost' in card.keys():
                    transfer_to_db[id]['*mana_cost'] = card['mana_cost']
                if 'cmc' in card.keys():
                    transfer_to_db[id]['*cmc'] = card['cmc']
                if 'type_line' in card.keys():
                    transfer_to_db[id]['*type_id'] = card['type_line']
                if 'oracle_text' in card.keys():
                    transfer_to_db[id]['*card_text'] = card['oracle_text']
                if 'colors' in card.keys():
                    transfer_to_db[id]['*card_color'] = card['colors']
                if 'keywords' in card.keys():
                    transfer_to_db[id]['*card_keywords'] = card['keywords']
                if 'set_name' in card.keys():
                    transfer_to_db[id]['*set_name'] = card['set_name']
                if 'power' in card.keys():
                    transfer_to_db[id]['*power'] = card['power']
                if 'toughness' in card.keys():
                    transfer_to_db[id]['*toughness'] = card['toughness']
                if 'collector_number' in card.keys():
                    transfer_to_db[id]['*collection_number'] = card['collector_number']
                if 'rarity' in card.keys():
                    transfer_to_db[id]['*rarity_id'] = card['rarity']
                if 'flavor_text' in card.keys():
                    transfer_to_db[id]['*flavor_text'] = card['flavor_text']
                if 'artist' in card.keys():
                    transfer_to_db[id]['*artist'] = card['artist']
                if 'prices' in card.keys():
                    if 'usd' in card['prices'].keys():
                        transfer_to_db[id]['*price'] = card['prices']['usd']
            # if there is no scryfall oracle id, there is no way to link to mtg json data so skip it
            else:
                continue

    # close scryfall data
    json_file.close()
    return transfer_to_db
    """"""
    For reference from above with Scryfall
    --------------------------------------
    ROOT_FILE = settings.STATIC_ROOT + '\main\card_data\scryfall_data.json'
    json_data = open(ROOT_FILE, encoding='utf8')
    json_load = json.load(json_data)
    with open(ROOT_FILE, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
        for card in data:
    # open MTGJSON data and load
    mtgjson = open(settings.STATIC_ROOT + '\main\card_data\'mtg_json_cards_data', 'r')
    data = json.load(mtgjson)  # this is a dict of the following format:  key='card name', value={<dictionary of card info>}
    for key, card in zip(data.keys(), data.values()):
        if card['scryfallOracleId']:
            # if we have a match in the scryfall data
            if card['scryfallOracleId'] in transfer_to_db.keys():
                dict_entry = transfer_to_db[card['scryfallOracleId']]
                # add items special to MTG
                if 'purchaseUrls' in card.keys():
                    if 'cardmarket' in card['purchaseUrls'].keys():
                        dict_entry['purchase_urls'] = {}
                        dict_entry['purchase_urls']['card_market'] = card['purchaseUrls']['cardmarket']
                    if 'tcgplayer' in card['purchaseUrls'].keys():
                        if 'purchase_urls' not in dict_entry.keys():
                            dict_entry['purchase_urls'] = {}
                            dict_entry['purchase_urls']['tcg_player'] = card['purchaseUrls']['tcgplayer']
                    if 'mtgstocks' in card['purchaseUrls'].keys():
                        if 'purchase_urls' not in dict_entry.keys():
                            dict_entry['purchase_urls'] = {}
                            dict_entry['purchase_urls']['mtg_stocks'] = card['purchaseUrls']['mtgstocks']
                # save MTG JSON uuid in case we want to use that to join with more data later
                if 'uuid' in card.keys():
                    dict_entry['uuid'] = card['uuid']

                # fill in any missing data not gotten from scryfall
                if 'name' not in dict_entry.keys() and 'name' in card.keys():
                    dict_entry['name'] = card['name']
                if 'mana_cost' not in dict_entry.keys() and 'mana_cost' in card.keys():
                    dict_entry['mana_cost'] = card['mana_cost']
                if 'type' not in dict_entry.keys() and 'type' in card.keys():
                    dict_entry['type'] = card['type']
                if 'colors' not in dict_entry.keys() and 'colors' in card.keys():
                    dict_entry['colors'] = card['colors']
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
                    transfer_to_db[id]['text'] = card['text']
                if 'purchaseUrls' in card.keys():
                    if 'cardmarket' in card['purchaseUrls'].keys():
                        transfer_to_db[id]['purchase_urls']['card_market'] = card['purchaseUrls']['cardmarket']
                    if 'tcgplayer' in card['purchaseUrls'].keys():
                        transfer_to_db[id]['purchase_urls']['tcg_player'] = card['purchaseUrls']['tcgplayer']
                    if 'mtgstocks' in card['purchaseUrls'].keys():
                        transfer_to_db[id]['purchase_urls']['mtg_stocks'] = card['purchaseUrls']['mtgstocks']
                # save MTG JSON uuid in case we want to use that to join with more data later
                if 'uuid' in card.keys():
                    transfer_to_db[id]['uuid'] = card['uuid']
                if 'name' in card.keys():
                    transfer_to_db[id]['name'] = card['name']
                if 'mana_cost' in card.keys():
                    transfer_to_db[id]['mana_cost'] = card['mana_cost']
                if 'type' in card.keys():
                    transfer_to_db[id]['type'] = card['type']
                if 'colors' in card.keys():
                    transfer_to_db[id]['colors'] = card['colors']
                if 'power' in card.keys():
                    transfer_to_db[id]['power'] = card['power']
                if 'toughness' in card.keys():
                    transfer_to_db[id]['toughness'] = card['toughness']
            # if there is no scryfall id we can't match it to the other data, so skip

            #dict_entry['purchase_urls']['card_market']
        else:
            continue
    mtgjson.close()
    #wait = 3
    """