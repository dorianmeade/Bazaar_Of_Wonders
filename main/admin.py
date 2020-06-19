from django.contrib import admin
from .models import Card_Rarity,Card_Type,Card_Color,Card,Location,Seller,Bazaar_User,Listing,Notification,Collection,Collection_Content

class CardAdmin(admin.ModelAdmin):
     fieldsets = (
        (None, {
            'fields': ('name', 'type_id', 'color_id', 'mana_cost')
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('card_image_loc', 'power', 'toughness', 'card_text', 'flavor_text', 'rarity_id', 'set_name', 'artist', 'collection_number')
        }),
    )

# Register your models here.
admin.site.register(Card_Rarity)
admin.site.register(Card_Type)
admin.site.register(Card_Color)
admin.site.register(Card, CardAdmin)
admin.site.register(Location)
admin.site.register(Seller)
admin.site.register(Bazaar_User)
admin.site.register(Listing)
admin.site.register(Notification)
admin.site.register(Collection)
admin.site.register(Collection_Content)



