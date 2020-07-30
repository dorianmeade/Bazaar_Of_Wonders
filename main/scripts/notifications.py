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
notifications = Notification.objects.all()
# queryset of listings that match the card in notif flag

for n in notifications:
    listings = Listing.objects.filter(product_id=n.card_id)
    for l in listings:
        # if listing price is lower than price flag
        if l.price < n.price_threshold:
            # send email
            text = "Hello {0},\r\n\nThis email is to notify you that there has been a price drop on {1}, " \
                   "and it is now offered for ${2}!\r\n\nLink to buy: {3}\r\n\n" \
                   "Have a great day!\r\n--The Bazaar of Wonders Team".\
                format(n.auth_user_id.first_name, l.product_name, l.price, l.product_id.tcg_player_purchase_url)
            send_mail('Price drop!', text, settings.DEFAULT_FROM_EMAIL, [n.auth_user_id.email], fail_silently=False)
            print("Email sent to {0}".format(n.auth_user_id.email))
            print("Email said {0}".format(text))
            # then deleted notif flag
            Notification.objects.get(id=n.id).delete()
            break  # don't spam them with a bunch of price drop emails
