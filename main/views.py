from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request = request,
                  template_name='main/home.html',
                  )

def register(request):
    return HttpResponse("hello register")

def login_request(request):
    return HttpResponse("hello login")
