from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Bazaar_User, Seller, User_Preferences
from django.utils.safestring import mark_safe
from django.urls import reverse

# new user registration form
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address", help_text="Email address cannot be associated with another Bazaar of Wonders account.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user   


# listing display filter form for home view
class SearchForm(forms.Form):
    CARD_TYPES = [
    ('NO_VALUE','Any Card Type'),
    ('artifact', 'Artifact'),
    ('creature', 'Creature'),
    ('enchantment', 'Enchantment'),
    ('instant', 'Instant'),
    ('land', 'Land'),
    ('planeswalker', 'Planeswalker'),
    ('tribal', 'Tribal'),
    ('sorcery', 'Sorcery'),
    ]

    CARD_RARITIES = [
    ('NO_VALUE', 'Any Card Rarity'),
    ('rare', 'Rare'),
    ('common', 'Common'),
    ('uncommon', 'Uncommon'),
    ('mythic', 'Mythic'),
    ]

    SORT_ORDERS = {
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    }

    SORT_BY = {
        ('card_name', 'Card Name'),
        ('card_rarity', 'Card Rarity'),
        ('card_type', 'Card Type'),
    }

    card_name = forms.CharField(max_length=200, required=False)
    card_type = forms.CharField(label='Card Type:', widget=forms.Select(choices=CARD_TYPES,
                                                                        attrs={'class': 'dropdown-trigger btn',
                                                                               'style': 'background-color: '
                                                                                        'darkolivegreen; color: black; '
                                                                                        'font-weight: bold'}))
    card_rarity = forms.CharField(label='Card Rarity:', widget=forms.Select(choices=CARD_RARITIES,
                                                                            attrs={'class': 'dropdown-trigger btn',
                                                                                   'style': 'background-color: '
                                                                                            'darkolivegreen; '
                                                                                            'color: black; '
                                                                                            'font-weight: bold'}),
                                  initial='NO_VALUE')
    sort_by_choice = forms.CharField(label='Sort Criteria:', widget=forms.Select(choices=SORT_BY,
                                                                                 attrs={'class': 'dropdown-trigger btn',
                                                                                        'style': 'background-color: '
                                                                                                 'darkolivegreen; '
                                                                                                 'color: black; '
                                                                                                 'font-weight: bold'}),
                                     initial='card_name')
    sorting_order = forms.CharField(label='Sort Ordering:', widget=forms.Select(choices=SORT_ORDERS,
                                                                                attrs={'class': 'dropdown-trigger btn',
                                                                                       'style': 'background-color: '
                                                                                                'darkolivegreen; '
                                                                                                'color: black; '
                                                                                                'font-weight: bold'}),
                                    initial='ascending')


# listing display filter form for collection view
class CollectionSearchForm(forms.Form):
    CARD_TYPES = [
    ('NO_VALUE','Any Card Type'),
    ('artifact', 'Artifact'),
    ('creature', 'Creature'),
    ('enchantment', 'Enchantment'),
    ('instant', 'Instant'),
    ('land', 'Land'),
    ('planeswalker', 'Planeswalker'),
    ('tribal', 'Tribal'),
    ('sorcery', 'Sorcery'),
    ]

    CARD_RARITIES = [
    ('NO_VALUE','Any Card Rarity'),
    ('rare', 'Rare'),
    ('common', 'Common'),
    ('uncommon', 'Uncommon'),
    ('mythic', 'Mythic'),
    ]

    SORT_ORDERS = {
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    }

    SORT_BY = {
        ('card_name', 'Card Name'),
        ('card_rarity', 'Card Rarity'),
        ('card_type', 'Card Type'),
    }

    YES_NO = {
        ('yes', 'Yes'),
        ('no', 'No'),
    }

    card_name = forms.CharField(max_length=200, required=False)
    card_type = forms.CharField(label='Card Type:', widget=forms.Select(choices=CARD_TYPES,
                                                                        attrs={'class': 'dropdown-trigger btn',
                                                                               'style': 'background-color: '
                                                                                        'darkolivegreen; color: black; '
                                                                                        'font-weight: bold'}))
    card_rarity = forms.CharField(label='Card Rarity:', widget=forms.Select(choices=CARD_RARITIES,
                                                                            attrs={'class': 'dropdown-trigger btn',
                                                                                   'style': 'background-color: '
                                                                                            'darkolivegreen; '
                                                                                            'color: black; '
                                                                                            'font-weight: bold'}),
                                  initial='NO_VALUE')
    own = forms.CharField(label='Show cards I own:', widget=forms.Select(choices=YES_NO,
                                                                         attrs={'class': 'dropdown-trigger btn',
                                                                                'style': 'background-color: '
                                                                                         'darkolivegreen; '
                                                                                         'color: black; '
                                                                                         'font-weight: bold'}),
                          initial='yes')
    dont_own = forms.CharField(label='Show cards I don\'t own:',
                               widget=forms.Select(choices=YES_NO, attrs={'class': 'dropdown-trigger btn',
                                                                          'style': 'background-color: '
                                                                                   'darkolivegreen; color: black; '
                                                                                   'font-weight: bold'}),
                               initial='yes')
    sort_by_choice = forms.CharField(label='Sort Criteria:', widget=forms.Select(choices=SORT_BY,
                                                                                 attrs={'class': 'dropdown-trigger btn',
                                                                                        'style': 'background-color: '
                                                                                                 'darkolivegreen; '
                                                                                                 'color: black; '
                                                                                                 'font-weight: bold'}),
                                     initial='card_name')
    sorting_order = forms.CharField(label='Sort Ordering:', widget=forms.Select(choices=SORT_ORDERS,
                                                                                attrs={'class': 'dropdown-trigger btn',
                                                                                       'style': 'background-color: '
                                                                                                'darkolivegreen; '
                                                                                                'color: black; '
                                                                                                'font-weight: bold'}),
                                    initial='ascending')


# user portal - edit account info form
class EditUserForm(UserChangeForm):
    password = forms.CharField(max_length=255, help_text=mark_safe("<a href='/account/edit/password'>Click to change your password</a>."))
    
    class Meta: 
        model = User
        fields = (
            'username', 
            'password',
            'email',
            'first_name',
            'last_name',
        )
        labels = {
            "email": "Email address",
        }
        help_texts = {
            'username': None,
        }


#user portal - edit account info extension
class UpdateUserForm(forms.ModelForm):
    class Meta: 
        model = Bazaar_User  
        fields = (
            'location',
        )

#user portal - edit user seller info 
class UpdateSellerForm(forms.ModelForm):
    disabled_fields = ['seller_key', 'seller_type', 'completed_sales']

    class Meta: 
        model = Seller
        fields = (
            'seller_key',
            'seller_name',
            'seller_type',
            'completed_sales',
            'location',
        )
        labels = {
            "seller_key": "Usernname",
            "seller_name": "Trader display name",
            "seller_type": "Trader status",
        }
    
    def __init__(self, *args, **kwargs):
        super(UpdateSellerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.disabled_fields:
                self.fields[field].disabled = True
        else:
            self.fields['reviewed'].disabled = True

#user portal - preferences form
class UpdatePreferencesForm(forms.Form):  
    TRUE_FALSE_CHOICES = {
        (True, 'Yes'),
        (False, 'No'),
    }
    email_notif = forms.CharField(label='Allow Bazaar of Wonders to send you email notifications', widget=forms.Select(choices=TRUE_FALSE_CHOICES,
                                                                        attrs={'class': 'dropdown-trigger btn',
                                                                                'style': 'color: black; background-color: orange;'}))   


    subscribe_email = forms.CharField(label='Recieve email newsletter', widget=forms.Select(choices=TRUE_FALSE_CHOICES,
                                                                        attrs={'class': 'dropdown-trigger btn',
                                                                                'style': 'color: black; background-color: orange;'}))   

    view_email = forms.CharField(label='Allow other Bazaar Traders to view your profile', widget=forms.Select(choices=TRUE_FALSE_CHOICES,
                                                                        attrs={'class': 'dropdown-trigger btn',
                                                                                'style': 'color: black; background-color: orange;'}))   



