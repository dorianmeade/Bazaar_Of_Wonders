from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

app_name = 'main'  # here for namespacing of urls.

#map url path to function in views.py
urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login_req"),
    path("logout", views.logout_request, name="logout_req"),
    path("details", views.card_view, name="details"),
    path("details/<int:pk>", views.card_view, name="detailsID"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("collection", views.collection, name="collection"),
    path("notifications", views.notifications, name="notifications"),
]