from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FilterForm, NewUserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

#homepage view
def home(request):
    return render(request = request,
                  template_name='main/home.html',
                  )

#registration page
def register(request):
    #upon submit
    if request.method == "POST":
        form = NewUserForm(request.POST)
        #validate user input, create new user account, login user
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:home")
        #error, don't create new user account
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            
            return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})
    form  = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

#login page/form
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
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
    return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})

#function for filtering cards in the working
def filter_request(request):
    context = {}
    context['form'] = FilterForm()
    return render( request, "navbaritems.html", context) 

#function to log user out of system
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out succesfully!")
    return redirect("main:home")



