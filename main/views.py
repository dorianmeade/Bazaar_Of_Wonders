from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from .forms import NewUserForm,searchForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import Card, Listing, Collection, Collection_Content,Card_Type,Card_Rarity

# homepage view
def home(request):
    # upon submit
    if request.method == "POST":
        form = searchForm(request.POST)
        # validate user input, create new user account, login user
        if form.is_valid():
            CardManager = Card.objects
            #Filtering by name (if name not specified, this will return all cards)
            cards = CardManager.filter(name__icontains = form.cleaned_data['card_name'])

            #Filter by Card Type 
            if form.cleaned_data['card_type'] != 'NO_VALUE':
                cards = cards.filter(type_id__card_type__iexact = form.cleaned_data['card_type'])

            #Filter by Card Rarity  
            if form.cleaned_data['card_rarity'] != 'NO_VALUE':
                cards = cards.filter(rarity_id__card_rarity__iexact = form.cleaned_data['card_rarity'])

            #Implement sorts 
            if form.cleaned_data['sort_by_choice'] == 'card_name':
                sort_param = "name"
            elif form.cleaned_data['sort_by_choice'] == 'card_rarity':
                sort_param = "rarity_id__card_rarity"
            elif form.cleaned_data['sort_by_choice'] == 'card_type':
                sort_param = "type_id__card_type"

            if form.cleaned_data['sorting_order'] == "descending":
                sort_param = "-" + sort_param

            #Sort the QuerySet per thje parameter
            cards = cards.order_by(sort_param)

            return render(request=request,
                        template_name='main/search/search.html',
                        context={"data": cards, "form": form})
        else:
            #Restart the form submission process with bound data from previous request 
            form = searchForm(request.POST)            
            return render(request = request,
                          template_name = "main/search/search.html",
                          context={"data": cards, "form": form})

    elif request.method == "GET":
            form = searchForm
            return render(request = request,
                          template_name = "main/home.html",
                          context={"data": Card.objects.all(),"form":form})  
    else:
        cards = Card.objects.all()
        #display only 25 cards per page
        paginator = Paginator(cards, 25)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_obj = paginator.page(paginator.num_pages)

        form = searchForm
        return render(request=request,
                    template_name='main/home.html',
                    # load necessary schemas
                    context={'data': page_obj,'form': form})

# registration page form
def register(request):
    # upon submit
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # validate user input, create new user account, login user
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:home")
        # error, don't create new user account
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            
            return render(request=request,
                          template_name="main/registration/register.html",
                          context={"form": form})
    form = NewUserForm
    return render(request=request,
                  template_name="main/registration/register.html",
                  context={"form": form})


# login page/form
def login_request(request):
    # upon form submit
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        # validate user input
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # authenticate user in db
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request,
                  template_name="main/registration/login.html",
                  context={"form": form})


# user collection and notification management
def collection(request):
    # if a user is logged in see if they have a collection
    if request.user.is_authenticated:
        users_collection = None
        cards_in_collection = []
        try:
            users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
        except Collection.DoesNotExist:
            pass
        # if the user has a collection, get it
        if users_collection:
            collection_content, cards_in_collection = [], []
            try:
                collection_content = Collection_Content.objects.filter(collection_id=users_collection.id)
            except Collection_Content.DoesNotExist:
                pass
            for item in collection_content:
                card = Card.objects.get(product_id=item.card_id_id)
                own = item.obtained
                cards_in_collection.append({'card': card, 'own': own})
    return render(request=request,
                  template_name='main/collection_and_notification_portal.html',
                  context={'users_collection': cards_in_collection})


# user collection and notification management
def notifications(request):
    return render(request=request,
                  template_name='main/notifications.html',
                  context={})


# log user out of system
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out succesfully!")
    return redirect("main:home")

 
# card details page
def card_view(request, selected=None):
    # get primary key from url
    card_id = request.GET.get('selected', '')

    try: 
        # get card object from pk
        card = Card.objects.get(product_id=card_id)
        card_saved = False

        # get listing objects for this card
        listings = Listing.objects.filter(product_id=card_id)

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            collection_content = []
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # if the user has a collection, get it
            if users_collection:
                try:
                    collection_content = Collection_Content.objects.filter(collection_id=users_collection.id)
                except Collection_Content.DoesNotExist:
                    pass
                # check to see if selected card is in collection
                for collected_card in collection_content:
                    if collected_card.card_id_id == card.product_id:
                        card_saved = True  # found card
                        break
        return render(request=request,
                      template_name="main/details.html",
                      context={"c": card, 'card_saved': card_saved, "l": listings}
                      )
    except Card.DoesNotExist:
        return render(request=request,
                      template_name="main/details.html",
                      )
    except ValueError:
        return render(request=request,
                      template_name="main/details.html",
                      )


def add_to_collection_view(request, selected=None):
    try:
        # get card object from pk
        card = Card.objects.get(product_id=request.GET.get('selected', ''))

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # if the user has a collection, and it isn't already in their collection (should never happen, but jic)
            # add this card to it
            if users_collection:
                card_there_already = None
                try:
                    card_there_already = Collection_Content.objects.get(card_id=card.product_id,
                                                                        collection_id=users_collection)
                except Collection_Content.DoesNotExist:
                    pass
                if not card_there_already:
                    Collection_Content(collection_id=users_collection, card_id=card, obtained=False).save()
            # if the user does not have a collection, make them one and add this card to it
            else:
                Collection(owning_auth_user_id=request.user.id,
                           collection_name="{0}'s Collection".format(request.user.username)).save()
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
                Collection_Content(collection_id=users_collection, card_id=card, obtained=False).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Card.DoesNotExist:
        return redirect(to=card_view(request, selected=selected))
    except ValueError:
        return redirect(to=card_view(request, selected=selected))


def remove_from_collection_view(request, selected=None):
    try:
        # get card object from pk
        card = Card.objects.get(product_id=request.GET.get('selected', ''))

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # if the user has a collection, the card is in their collection, done
            if users_collection:
                card_in_collection = None
                try:
                    card_in_collection = Collection_Content.objects.get(card_id=card.product_id,
                                                                        collection_id=users_collection)
                except Collection_Content.DoesNotExist:
                    pass
                if card_in_collection:
                    card_in_collection.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Card.DoesNotExist:
        return redirect(to=card_view(request, selected=selected))
    except ValueError:
        return redirect(to=card_view(request, selected=selected))


def toggle_ownership_view(request, selected=None):
    try:
        # get card object from pk
        card = Card.objects.get(product_id=request.GET.get('selected', ''))

        # if a user is logged in see if they have a collection
        if request.user.is_authenticated:
            users_collection = None
            try:
                users_collection = Collection.objects.get(owning_auth_user_id=request.user.id)
            except Collection.DoesNotExist:
                pass
            # find the card in the collection and change the value
            if users_collection:
                card_of_interest = None
                try:
                    card_of_interest = Collection_Content.objects.get(card_id=card.product_id,
                                                                      collection_id=users_collection)
                except Collection_Content.DoesNotExist:
                    pass
                if card_of_interest:
                    desired_value = not card_of_interest.obtained
                    Collection_Content.objects.filter(card_id=card.product_id, collection_id=users_collection).\
                        update(obtained=desired_value)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Card.DoesNotExist:
        return redirect(to=card_view(request, selected=selected))
    except ValueError:
        return redirect(to=card_view(request, selected=selected))

def search(request):
    # upon submit
    if request.method == "POST":
        form = searchForm(request.POST)
        # validate user input, create new user account, login user
        if form.is_valid():
            CardManager = Card.objects
            #Filtering by name (if name not specified, this will return all cards)
            cards = CardManager.filter(name__icontains = form.cleaned_data['card_name'])

            #Filter by Card Type 
            if form.cleaned_data['card_type'] != 'NO_VALUE':
                cards = cards.filter(type_id__card_type__iexact = form.cleaned_data['card_type'])

            #Filter by Card Rarity  
            if form.cleaned_data['card_rarity'] != 'NO_VALUE':
                cards = cards.filter(rarity_id__card_rarity__iexact = form.cleaned_data['card_rarity'])

            #Implement sorts 
            if form.cleaned_data['sort_by_choice'] == 'card_name':
                sort_param = "name"
            elif form.cleaned_data['sort_by_choice'] == 'card_rarity':
                sort_param = "rarity_id__card_rarity"
            elif form.cleaned_data['sort_by_choice'] == 'card_type':
                sort_param = "type_id__card_type"

            if form.cleaned_data['sorting_order'] == "descending":
                sort_param = "-" + sort_param

            #Sort the QuerySet per thje parameter
            cards = cards.order_by(sort_param)

            return render(request=request,
                        template_name='main/home.html',
                        context={"data": cards, "form": form})
        else:
            #Restart the form submission process with bound data from previous request 
            form = searchForm(request.POST)            
            return render(request = request,
                          template_name = "main/home.html",
                          context={"data": Card.objects.all(), "form": form})

    elif request.method == "GET":
            form = searchForm
            return render(request = request,
                          template_name = "main/home.html",
                          context={"data": Card.objects.all(),"form":form})                    