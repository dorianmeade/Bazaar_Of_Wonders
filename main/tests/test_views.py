from django.test import TestCase
from main.models import Card, Card_Type, Card_Rarity, Listing, Seller, Location

class HomePageTest(TestCase): #view or template??
    def setUp(self):
        #card obj
        type_inst = Card_Type.objects.create(card_type='land')
        rarity_inst = Card_Rarity.objects.create(card_rarity='rare')     
        card_inst = Card.objects.create(product_id=99, name='cardTest', type_id=type_inst, card_color='blue', mana_cost='99', card_image_loc='uk', power=-1, toughness=-1, card_text='uk', flavor_text='UK', rarity_id=rarity_inst, set_name='uk', artist='uk', collection_number=-1)
        #seller obj
        location_inst = Location.objects.create(location='USA')
        seller_inst = Seller.objects.create(seller_key='123abc', seller_name='sellerTest', seller_type='good', location_id=location_inst, completed_sales=0)
        #listing obj
        listing_inst = Listing.objects.create(product_id=card_inst, product_name='cardTest', product_line='magic', set_name='UNH', price=2.00, quantity=1, condition='good', seller_key=seller_inst, seller_type='good', sponsored=False, user_listing=False, selling_user_id=-1)

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    #check for listing displayed on homepage 
    def test_card_listings(self):
        response = self.client.get('/')
        self.assertContains(response, 'card-testing')