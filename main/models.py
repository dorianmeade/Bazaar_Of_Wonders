from django.db import models
from django.urls import reverse

class Card_Rarity(models.Model):
    card_rarity = models.CharField(max_length=200, unique=True) 
    def __str__(self):
        return self.card_rarity

class Card_Type(models.Model):
    card_type = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.card_type

class Card(models.Model):
    #Primary Key
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200) 
    type_id = models.ForeignKey('Card_Type',on_delete=models.CASCADE)
    card_color = models.CharField(max_length=200,default='N/A')
    mana_cost = models.CharField(max_length=200)
    card_image_loc = models.CharField(max_length=800)
    power = models.IntegerField() 
    toughness = models.IntegerField()
    card_text = models.CharField(max_length=4000)
    flavor_text = models.CharField(max_length=4000)
    rarity_id = models.ForeignKey('Card_Rarity',on_delete=models.CASCADE)
    set_name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    collection_number = models.IntegerField()
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('main:card_view', args=[str(self.product_id)])

class Location(models.Model):
    location = models.CharField(max_length=200) 

class Seller(models.Model):
    seller_key = models.CharField(max_length=200,primary_key=True)
    seller_name = models.CharField(max_length=200)
    seller_type = models.CharField(max_length=200)
    location_id = models.ForeignKey('Location',on_delete=models.CASCADE)
    completed_sales = models.BigIntegerField()

class Bazaar_User(models.Model):
    auth_user_id = models.IntegerField() #Researching how to properly do an FK on a table not represented by a model (auth_user)
    location_id = models.ForeignKey('Location',on_delete=models.CASCADE)
    completed_sales = models.BigIntegerField()

class Listing(models.Model):
    product_id = models.ForeignKey('Card',on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_line = models.CharField(max_length=50)
    set_name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    condition = models.CharField(max_length=200)
    seller_key = models.ForeignKey('Seller',on_delete=models.CASCADE)
    seller_type = models.CharField(max_length=200)
    sponsored = models.BooleanField()
    user_listing = models.BooleanField()
    selling_user_id = models.IntegerField() #Researching how to properly do an FK on a table not represented by a model (auth_user)
    def __str__(self):
        return self.product_name
    
class Notification(models.Model):
    auth_user_id = models.IntegerField() #Researching how to properly do an FK on a table not represented by a model (auth_user)
    card_id = models.ForeignKey('Card',on_delete=models.CASCADE)
    price_threshold = models.FloatField()
    less_than_flag = models.BooleanField()
    greater_than_flag = models.BooleanField()
    equal_flag = models.BooleanField()
    seller_key = models.ForeignKey('Seller',on_delete=models.CASCADE)
    selling_auth_user_id = models.IntegerField() #Researching how to properly do an FK on a table not represented by a model (auth_user)
    models.ForeignKey('Card_Rarity',on_delete=models.CASCADE)

class Collection(models.Model):
    owning_auth_user_id = models.IntegerField() #Researching how to properly do an FK on a table not represented by a model (auth_user) 
    collection_name = models.CharField(max_length=200)

class Collection_Content(models.Model):
    collection_id = models.ForeignKey('Collection',on_delete=models.CASCADE)
    card_id = models.ForeignKey('Card',on_delete=models.CASCADE) 
    obtained = models.BooleanField()