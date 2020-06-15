from django.urls import path, include
from . import views

app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("", views.filter_request)
]