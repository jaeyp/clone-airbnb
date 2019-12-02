from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # remove label suffix ':'
        # https://medium.com/@MatheusCAS/overriding-globally-field-label-suffix-in-django-ed3ffb10af7
        kwargs.setdefault("label_suffix", "")
        super(CreateReviewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )
        widgets = {
            "review": forms.Textarea(attrs={"class": "reviewField"}),
            "accuracy": forms.Select(attrs={"class": "reviewField"}),
            "communication": forms.Select(attrs={"class": "reviewField"}),
            "cleanliness": forms.Select(attrs={"class": "reviewField"}),
            "location": forms.Select(attrs={"class": "reviewField"}),
            "check_in": forms.Select(attrs={"class": "reviewField"}),
            "value": forms.Select(attrs={"class": "reviewField"}),
        }

    # Intercepting user data and edit it before save
    # https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#the-save-method
    def save(self, *args, **kwargs):
        #  If you call save() with commit=False,
        #  then it will return an object that hasn’t yet been saved to the database.
        review = super().save(commit=False)
        return review  # return a review that hasn’t yet been saved to the database.
