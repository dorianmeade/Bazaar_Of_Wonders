import os
import sys
from django.conf import settings
from django import setup
sys.path.append("../../../Bazaar_Of_Wonders")
os.environ["DJANGO_SETTINGS_MODULE"] = "bazaar_of_wonders.settings"
setup()
from django.core.mail import send_mail
from main.models import Notification, Listing

# get notification flag object
notifications = Notification.objects.all().filter(auth_user_id__first_name__exact='Kelsey')
# queryset of listings that match the card in notif flag

for n in notifications:
    listing = Listing.objects.filter(product_id=n.card_id)[0]
    print('original price: {0}'.format(listing.price))
    print('price threshold: {0}'.format(n.price_threshold))
    listing.price = n.price_threshold - 0.10
    listing.save(update_fields=['price'])
    print('new price: {0}'.format(listing.price))
