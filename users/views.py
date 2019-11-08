from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout  # , LoginView
from . import forms, models

""" Implementation of LoginView """

# 1. Easiest way to have LoginView
# Using django.contrib.auth.LoginView
# Ref: https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.views.LoginView
# But you can NOT have email as username with django.contrib.auth.LoginView

""" Example
class LoginView(LoginView):
    pass
"""

# 2. Easier way
# Using AuthenticationForm (django.contrib.auth.forms.AuthenticationForm)
# Ref: https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm
# cf. class PasswordResetForm: we even can send email a link to reset a user's password!!

""" Example
"""

# 3. A little bit easier way (Preferred)
# Using FormView (django.views.generic.edit.FormView)
# Ref: https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-editing/#django.views.generic.edit.FormView
# Attributes: http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/FormView/


class LoginView(FormView):
    # FormView inherits TemplateResponseMixin so template_name can be used here.
    template_name = "users/login.html"
    # form_class: The form class to instantiate.
    form_class = forms.LoginForm
    # success_url: The URL to redirect to when the form is successfully processed.
    # reverse_lazy(): A lazily evaluated version of reverse().
    # It is useful for when you need to use a URL reversal before your project’s URLConf is loaded.
    success_url = reverse_lazy("core:home")  # reverse("core:home")
    # initial: A dictionary containing initial data for the form.
    initial = {"email": "jp.inseoul@gmail.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        # The default form_valid() simply redirects to the success_url.
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {"first_name": "Jaey", "last_name": "Park", "email": "jp.inseoul@gmail.com"}

    # form is valid
    def form_valid(self, form):
        # create account
        form.save()

        # login immediately
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        # email verification
        user.verify_email()
        return super().form_valid(form)  # redirects to the success_url.


def complete_verification(request, key):
    try:
        user = models.User.objects.get(verification_code=key)
        user.email_verified = True
        user.verification_code = ""  # clear code
        user.save()
        # to do: add success message
        # Django Messages Framework: https://docs.djangoproject.com/en/2.2/ref/contrib/messages/
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# 4. Very manual way by defining get and post methods

""" Example
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "test@email.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Once we send form data to Django, it validates data.
            # if form data is valid without any errors, the cleaned_data dictionary of the form is set.
            print(form.cleaned_data)

            # Authentication - Login & Logout
            # https://docs.djangoproject.com/en/2.2/topics/auth/default/#authentication-in-web-requests
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
"""
