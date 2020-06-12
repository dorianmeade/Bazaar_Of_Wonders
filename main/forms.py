from django import forms

class FilterForm(forms.Form):
    filter_year = forms.BooleanField()

    