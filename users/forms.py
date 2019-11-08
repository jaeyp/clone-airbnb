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


class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmed = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password_confirmed(self):
        password = self.cleaned_data.get("password")
        password_confirmed = self.cleaned_data.get("password_confirmed")
        if password != password_confirmed:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()


# ModelForm
# For SignUpForm, inheriting forms.Form would be preferred since it usually takes more customizations.
# But, for the rest of forms, recommand to use ModelForm as much as you can. it's super helpful.
# Ref. https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/


""" class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    # we keep these password variables since User's password is an encrypted one
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmed = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password_confirmed(self):
        password = self.cleaned_data.get("password")
        password_confirmed = self.cleaned_data.get("password_confirmed")
        if password != password_confirmed:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#the-save-method
    def save(self, *args, **kwargs):
        #  If you call save() with commit=False,
        #  then it will return an object that hasn’t yet been saved to the database.
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save() """
