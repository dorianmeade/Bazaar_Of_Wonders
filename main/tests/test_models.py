from django.test import TestCase, RequestFactory
from main.models import Card, Card_Type, Card_Rarity, Listing, Seller, Location
'''
FIXME: determine schema functionality that needs to be tested?
        do we want to separate classes by schema
'''
class ModelTest(TestCase):
    def setUp(self):
        type_inst = Card_Type.objects.create(card_type='land')
        rarity_inst = Card_Rarity.objects.create(card_rarity='rare')     
        card_inst = Card.objects.create(product_id=99, name='testCard', type_id=type_inst, card_color='blue', mana_cost='99', card_image_loc='uk', power=-1, toughness=-1, card_text='uk', flavor_text='UK', rarity_id=rarity_inst, set_name='uk', artist='uk', collection_number=-1)      
        
        #seller obj
        location_inst = Location.objects.create(location='USA')
        seller_inst = Seller.objects.create(seller_key='123abc', seller_name='sellerTest', seller_type='good', location_id=location_inst, completed_sales=0)
        #listing obj
        listing_inst = Listing.objects.create(product_id=card_inst, product_name='cardTest', product_line='magic', set_name='UNH', price=2.00, quantity=1, condition='good', seller_key=seller_inst, seller_type='good', sponsored=False, user_listing=False, selling_user_id=-1)

    #test card obj retrieval
    def test_card_get(self):
        test_card = Card.objects.get(product_id=99)
        self.assertEqual(test_card.name, "testCard")
        self.assertEqual(test_card.type_id.card_type, "land")

    #test listing fk to card schema
    def test_listing_fk(self):
        test_card = Card.objects.get(product_id=99)
        test_listing = Listing.objects.get(product_name='cardTest')
        self.assertEqual(test_listing.product_id.name, test_card.name)



