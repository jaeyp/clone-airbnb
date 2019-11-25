from django import forms

# built-in authentication form
# Refs. https://docs.djangoproject.com/en/2.2/topics/auth/default/#module-django.contrib.auth.forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import password_validation as validator

from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

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
                # self.add_error("password", forms.ValidationError("Password is wrong"))

                # non_field_errors
                # https://docs.djangoproject.com/en/2.2/ref/forms/api/#django.forms.Form.non_field_errors
                self.add_error(None, forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            # raise forms.ValidationError("User does not exist")
            # self.add_error("email", forms.ValidationError("User does not exist"))
            self.add_error(None, forms.ValidationError("User does not exist"))

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


# SignUp Form derived and extended from Built-in UserCreationForm
# TODO: fixe save failure issue
class DerivedSignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.TextInput(attrs={"placeholder": "Email address"}),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Create password"}))
    password_confirmed = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("That email is already taken", code="existing_user")
        except models.User.DoesNotExist:
            print(email)
            return email

    def clean_password_confirmed(self):
        print("clean_password_confirmed")
        password = self.cleaned_data.get("password")
        password_confirmed = self.cleaned_data.get("password_confirmed")
        if password != password_confirmed:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            print(password)
            return password

    def save(self):
        print("DerivedSignUpForm - user save")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()


# Custom SignUp Form (preferred. - more customizable)
# In order to add more features, check source codes of built-in forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, ...
""" class SignUpForm(forms.Form):

    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"}), max_length=80)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last name"}), max_length=80)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Create password"}))
    password_confirmed = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))
    # password_confirmed = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Custom Form field validator/formatter
    # clean_<fieldname>() method
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password_confirmed(self):
        password = self.cleaned_data.get("password")
        password_confirmed = self.cleaned_data.get("password_confirmed")
        
        # https://docs.djangoproject.com/en/2.2/topics/auth/passwords/#django.contrib.auth.password_validation.validate_password
        validator.validate_password(password)

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
        user.save() """


# ModelForm
# For SignUpForm, inheriting forms.Form would be preferred since it usually takes more customizations.
# But, for the rest of forms, recommand to use ModelForm as much as you can. it's super helpful.
# Ref. https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.TextInput(attrs={"placeholder": "Email address"}),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Create password"}))
    password_confirmed = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("That email is already taken", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # https://docs.djangoproject.com/en/2.2/topics/auth/passwords/#django.contrib.auth.password_validation.validate_password
        validator.validate_password(password)
        return password

    def clean_password_confirmed(self):
        password = self.cleaned_data.get("password")
        if password is not None:
            password_confirmed = self.cleaned_data.get("password_confirmed")
            print(f"{password} == {password_confirmed}")

            if password != password_confirmed:
                raise forms.ValidationError("Password confirmation does not match", code="")
            else:
                return password

    # Intercepting user data and edit it before save
    # https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#the-save-method
    def save(self, *args, **kwargs):
        #  If you call save() with commit=False,
        #  then it will return an object that hasn’t yet been saved to the database.
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
