from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Custom Form field validator/formatter
    """ clean_<fieldname>() method
        The `clean_<fieldname>()` method is called on a form subclass – where <fieldname> is replaced with
            the name of the form field attribute.
        This method does any cleaning that is specific to that particular attribute,
            unrelated to the type of field that it is.
        check https://docs.djangoproject.com/en/2.2/ref/forms/validation/
    """

    # If you want to validate the field that depends on each other such as password1 & password2 for confirm,
    # You have to define `clean()` method instead of `clean_<fieldname>()` method
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # validate password here
        try:
            # this time, we use email as username
            user = models.User.objects.get(username=email)

            # check_password()
            # Returns True if the given raw string is the correct password for the user.
            # (This takes care of the password hashing in making the comparison.))
            if user.check_password(password):
                # return password
                return self.cleaned_data
            else:
                # raise forms.ValidationError("Password is wrong")
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            # raise forms.ValidationError("User does not exist")
            self.add_error("email", forms.ValidationError("User does not exist"))

    """ def clean_email(self):
        email = self.cleaned_data.get("email")

        # validate email here
        try:
            # this time, we use email as username
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # validate password here
        try:
            # this time, we use email as username
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is wrong")
        except models.User.DoesNotExist:
            pass """
