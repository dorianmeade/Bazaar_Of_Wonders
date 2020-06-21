from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .forms import NewUserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import Card, Listing, Bazaar_User

# homepage view
def home(request):
    return render(request=request,
                  template_name='main/home.html',
                  #load necessary schemas 
                  context={"cards": Card.objects.all, "listings": Listing.objects.all}
                  )

#registration page form
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
    return render(request=request,
                  template_name='main/collection_and_notification_portal.html',
                  context={})

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

#user account portal view
def member_view(request):
    return render(request = request,
                  template_name = "main/members.html",
                  )
 
#card details page
def card_view(request, selected=None):
    #get primary key from url
    cardID = request.GET.get('selected', '')
    try: 
        #get card object from pk
        card = Card.objects.get(product_id=cardID)
        return render(request=request,
                  template_name="main/details.html",
                  context={"c": card}
                )
    except Card.DoesNotExist:
        return render(request=request,
                      template_name="main/details.html",
                    )
    except ValueError:
        return render(request=request,
                      template_name="main/details.html",
                    )

