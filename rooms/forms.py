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


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    # Intercepting user data and edit it before save
    # https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#the-save-method

    # this is not a View, 'pk' is not passed into this form as arguments
    # So, we should pass pk manually through form.save() from form_valid() of View class (RoomPhotosAddView)
    """ def save(self, *args, **kwargs):
        pk = kwargs.get("pk")
        photo = super().save(commit=False) """

    def save(self, pk, *args, **kwargs):
        print(pk)
        # If you call save() with commit=False,
        # then it will return an object that hasn’t yet been saved to the database.
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()
