from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

app_name = 'main'  # here for namespacing of urls.

#map url path to function in views.py
urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("members", views.member_view, name="member"),
    path("details", views.card_view, name="details"),
    path("details/<slug:selected>", views.card_view, name="thiscard"),
    path("accounts/", include('django.contrib.auth.urls')),

]