from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#new user registration form
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user   




class searchForm(forms.Form):

    CARD_TYPES= [
    ('NO_VALUE','Pick a Card Type'),
    ('artifact', 'Artifact'),
    ('creature', 'Creature'),
    ('enchantment', 'Enchantment'),
    ('instant', 'Instant'),
    ('land', 'Land'),
    ('planeswalker', 'Planeswalker'),
    ('tribal', 'Tribal'),
    ('sorcery', 'Sorcery'),
    ]

    CARD_RARITIES= [
    ('NO_VALUE','Pick a Card Rarity'),
    ('rare', 'Rare'),
    ('common', 'Common')
    ]

    SORT_ORDERS = {
        ('ascending','Ascending'),
        ('descending','Descending')
    }

    SORT_BY = {
        ('card_name','Card Name'),
        ('card_rarity','Card Rarity'),
        ('card_type','Card Type'),
    }

    card_name = forms.CharField(max_length=200, required=False)
    card_type = forms.CharField(label='Card Type:', widget=forms.Select(choices=CARD_TYPES))
    card_rarity = forms.CharField(label='Card Rarity:', widget=forms.Select(choices=CARD_RARITIES),initial='NO_VALUE')
    sorting_order = forms.CharField(label='Sort Ordering:', widget=forms.Select(choices=SORT_ORDERS),initial='ascending')
    sort_by_choice = forms.CharField(label='Sort by:', widget=forms.Select(choices=SORT_BY),initial='card_name')





