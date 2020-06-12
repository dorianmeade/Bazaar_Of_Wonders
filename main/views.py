from django.shortcuts import render
from django.http import HttpResponse
from .forms import FilterForm

def home(request):
    return render(request = request,
                  template_name='main/home.html',
                  )

def register(request):
    return HttpResponse("hello register")

def login_request(request):
    return HttpResponse("hello login\nif new user, register")

def filter_request(request):
    context = {}
    context['form'] = FilterForm()
    return render( request, "navbaritems.html", context) 


