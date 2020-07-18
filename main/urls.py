from django.urls import path, include, re_path
from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'main'  # here for namespacing of urls.

# map url path to function in views.py
urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login_req"),
    path("logout", views.logout_request, name="logout_req"),
    path("details", views.card_view, name="details"),
    path("details/<int:pk>", views.card_view, name="detailsID"),
    path("collection", views.collection, name="collection"),
    path("notifications", views.notifications, name="notifications"),
    path("add_to_collection", views.add_to_collection_view, name="add_to_collection"),
    path("remove_from_collection", views.remove_from_collection_view, name="remove_from_collection"),
    path("toggle_ownership", views.toggle_ownership_view, name="toggle_ownership"),
    path("search", views.search, name="search"),
    path("account", views.profile, name="profile"),
    path("account/pref", views.preferences, name="preferences"),
    path("account/edit", views.edit, name="edit"),
    path("account/pref/edit", views.editpref, name="editpref"),
    path("account/sell", views.sell, name="sell"),
    path("account/sell/edit", views.editsell, name="editsell"),
    path("account/edit/password", views.changepass, name="changepass"),
    #path("passwordreset", views.resetpass, name="resetpass"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_change/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]
