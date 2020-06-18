from django.contrib import admin
from .models import Card_Rarity,Card_Type,Card_Color,Card,Location,Seller,Bazaar_User,Listing,Notification

# Register your models here.
admin.site.register(Card_Rarity)
admin.site.register(Card_Type)
admin.site.register(Card_Color)
admin.site.register(Card)
admin.site.register(Location)
admin.site.register(Seller)
admin.site.register(Bazaar_User)
admin.site.register(Listing)
admin.site.register(Notification)
