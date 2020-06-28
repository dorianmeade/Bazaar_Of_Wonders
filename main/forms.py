from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# new user registration form
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
