from django.urls import path, include
from . import views

app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("", views.filter_request)
]