from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail
from main.models import Notification, Listing, Card
from django.core import management
# from main.static.main.card_data.auto_parse_data import parse_data
# from main.static.main.card_data.auto_get_data import get_data

# not yet tested background function to notify users of price drop via email
@background(schedule=60*30)
def send_email_notif(id):
	#get notification flag object
    n = Notification.objects.get(id=id)
    #queryset of listings that match the card in notif flag
    l = Listing.objects.filter(product_id = n.card_id)
    #iterate the listings of that card
    for c in l:
        #if listing price is lower than price flag
        if c.price < n.price_threshold:
            #send email
            send_mail('Price drop!', 'test',settings.DEFAULT_FROM_EMAIL,n.auth_user_id.email,fail_silently=False)
            #then deleted notif flag
            Notification.objects.get(id=id).delete()


def update_data():

    # get_data()
    # parse_data()
    print("New data retrieved")

    management.call_command('loaddata', 'cards.json', verbosity=0)
    print("Cards updated")
    # management.call_command('loaddata', 'listings.json', verbosity=0)
    # print("Listings updated")
