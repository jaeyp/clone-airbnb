from django import forms

# third-party packages
# https://github.com/SmileyChris/django-countries#custom-forms
from django_countries.fields import CountryField
from . import models

# Check this reference!
# Django Forms: https://docs.djangoproject.com/en/2.2/ref/forms/


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="CA").formfield()
    price = forms.IntegerField(required=False)
    property_type = forms.ModelChoiceField(
        required=False, empty_label="Any Kind", queryset=models.PropertyType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False, help_text="How many people will be staying?")
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)

    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        # Widgets References: https://docs.djangoproject.com/en/2.2/ref/forms/widgets/
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False, queryset=models.Facility.objects.all(), widget=forms.CheckboxSelectMultiple
    )
