import os 
import sys
from django.conf import settings
from django import setup
os.environ["DJANGO_SETTINGS_MODULE"] = "bazaar_of_wonders.settings"
sys.path.append("../../../Bazaar_Of_Wonders")
setup()

from main.models import Notification, Listing
from django.core.mail import send_mail

for flag in Notification:
    #queryset of listings that match the card in notif flag
    l = Listing.objects.filter(product_id = flag.card_id)

    #iterate the listings of that card
    for c in l:
        #if listing price is lower than price flag 
        if c.price < flag.price_threshold:
            content = 'The price of' + c.card_id.name + 'has dropped to' + c.price 
            #send email
            send_mail('Price drop!', content,settings.DEFAULT_FROM_EMAIL,flag.auth_user_id.email,fail_silently=False)
            #then deleted notif flag
            flag.delete()

