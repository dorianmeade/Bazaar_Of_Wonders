from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Card_Rarity(models.Model):
    card_rarity = models.CharField(max_length=200, unique=True)

    # def __str__(self):
    # return self.card_rarity


class Card_Type(models.Model):
    card_type = models.CharField(max_length=200, unique=True)

    # def __str__(self):
    # return self.card_type


class Card(models.Model):
    # Primary Key
    product_id = models.CharField(max_length=200,primary_key=True)
    scryfall_id = models.CharField(max_length=200, null=True)
    mtg_json_uuid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    card_image_loc = models.CharField(max_length=800)
    mana_cost = models.CharField(max_length=200)
    converted_mana_cost = models.IntegerField()
    type_id = models.ForeignKey('Card_Type', on_delete=models.CASCADE)
    card_text = models.CharField(max_length=4000)
    card_color = models.CharField(max_length=200, default='N/A')
    card_keywords = models.CharField(max_length=200)
    set_name = models.CharField(max_length=200)
    power = models.IntegerField() 
    toughness = models.IntegerField()
    collection_number = models.IntegerField()
    rarity_id = models.ForeignKey('Card_Rarity', on_delete=models.CASCADE)
    flavor_text = models.CharField(max_length=4000)
    artist = models.CharField(max_length=200)
    card_market_purchase_url = models.CharField(max_length=2000, default="https://www.cardmarket.com/en")
    tcg_player_purchase_url = models.CharField(max_length=2000, default="https://www.tcgplayer.com/")
    mtg_stocks_purchase_url = models.CharField(max_length=2000, default="https://www.mtgstocks.com/news")
    last_updated = models.CharField(max_length=200, default=datetime.isoformat(datetime.now()))
    
    # def __str__(self):
    # return self.name

    def save(self, *args, **kwargs):
        rarity, _ = Card_Rarity.objects.get_or_create(card_rarity = self.card_rarity) # pylint: disable=maybe-no-member
        self.rarity = rarity
        type, _ = Card_Type.objects.get_or_create(card_type = self.card_type) # pylint: disable=maybe-no-member
        self.type = type
        super(Card, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('main:card_view', args=[str(self.product_id)])


class Seller(models.Model):
    seller_user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    seller_key = models.CharField(max_length=200, primary_key=True)
    seller_name = models.CharField(max_length=200)
    seller_type = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    completed_sales = models.BigIntegerField(default=0)


class Bazaar_User(models.Model):
    auth_user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=True, null=True)
    completed_sales = models.BigIntegerField(default=0)


class Listing(models.Model):
    product_id = models.ForeignKey('Card', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_line = models.CharField(max_length=50)
    set_name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    condition = models.CharField(max_length=200)
    seller_key = models.ForeignKey('Seller', on_delete=models.CASCADE)
    sponsored = models.BooleanField()
    user_listing = models.BooleanField()
    last_updated = models.CharField(max_length=200, default=datetime.isoformat(datetime.now()))

    # def __str__(self):
    # return self.product_name

class Notification(models.Model):
    auth_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = models.ForeignKey('Card', on_delete=models.CASCADE)
    price_threshold = models.FloatField()
    less_than_flag = models.BooleanField(default=True)
    greater_than_flag = models.BooleanField(default=False)
    equal_flag = models.BooleanField(default=False)
    # seller_key = models.ForeignKey('Seller', on_delete=models.CASCADE)

    class Meta:
        unique_together = (("auth_user_id", "card_id", "price_threshold"),)


class Collection(models.Model):
    owning_auth_user_id = models.IntegerField() # Researching how to properly do an FK on a table not represented by a model (auth_user)
    collection_name = models.CharField(max_length=200)


class Collection_Content(models.Model):
    collection_id = models.ForeignKey('Collection', on_delete=models.CASCADE)
    card_id = models.ForeignKey('Card', on_delete=models.CASCADE)
    obtained = models.BooleanField()


class User_Preferences(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notif = models.BooleanField(default=True)    
    subscribe_email = models.BooleanField(default=False)
    view_email = models.BooleanField(default=True)
