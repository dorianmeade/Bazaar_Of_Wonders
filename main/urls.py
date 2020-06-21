from django.urls import path, include
from . import views

app_name = 'main'  # here for namespacing of urls.

#map url path to function in views.py
urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("collection", views.collection_and_notification_portal, name="collection"),
    path("notifications", views.notifications, name="notifications"),
    path("card-details/<int:product_id>", views.card_view, name="card_view"),
]