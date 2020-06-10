from django.db import models
from datetime import datetime

class Card(models.Model):
    card_name = models.CharField(max_length=50)
    card_type = models.CharField(max_length=50)
    card_color = models.CharField(max_length=10)
    card_set = models.CharField(max_length=25)
    card_description = models.TextField()
    card_flavor = models.TextField()
    card_artist = models.CharField(max_length=25)
    card_year = models.CharField(max_length=25)

    def __str__(self):
        return self.card_name

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=50)
    vendor_contact = models.CharField(max_length=50)

    def __str__(self):
        return self.vendor_name

class Listing(models.Model):
    listing_card = models.ManyToManyField(Card)
    listing_vendor = models.ManyToManyField(Vendor)
    listing_time = models.DateTimeField('time', default=datetime.now)
    listing_price = models.CharField(max_length=6)

    class Meta:
        ordering = ['listing_price']    

    def __str__(self):
        return self.listing_card
