import requests
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout  # , LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.conf import settings
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
    initial = {"email": ""}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            user.login_method = models.User.LOGIN_EMAIL
            user.save()
            login(self.request, user)
            messages.success(self.request, f"Welcome, {user.first_name}!")

        # The default form_valid() simply redirects to the success_url.
        return super().form_valid(form)


def log_out(request):
    user = request.user
    messages.success(request, f"See you later, {user.first_name}!")
    logout(request)
    return redirect(reverse("core:home"))


# Custom SignUp Form View
class SignUpView(FormView):
    template_name = "users/signup.html"
    # form_class = forms.DerivedSignUpForm  # using built-in form
    form_class = forms.SignUpForm  # using cutom form
    success_url = reverse_lazy("core:home")
    initial = {"first_name": "", "last_name": "", "email": ""}

    # TODO: email verification scenario has been improved
    # form is valid
    def form_valid(self, form):
        # create account
        form.save()

        # login immediately
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            user.login_method = models.User.LOGIN_EMAIL
            user.save()
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


# TODO: integrate three social logins (github, google, facebook)
# def social_login(request, key):
#     pass


# OAuth: https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
def github_login(request):
    # 1. Request a user's GitHub identity
    client_id = settings.GITHUB_ID
    redirect_uri = settings.GITHUB_CALLBACK_URL
    return redirect(
        f"{settings.GITHUB_AUTHORIZATION_ENDPOINT}"
        + f"?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = settings.GITHUB_ID
        client_secret = settings.GITHUB_SECRET
        # 2. Users are redirected back to your site by GitHub
        code = request.GET.get("code", None)
        if code is not None:
            response = requests.post(
                settings.GITHUB_TOKEN_ENDPOINT,
                data={"client_id": client_id, "client_secret": client_secret, "code": code},
                headers={"Accept": "application/json"},
            )
            json_response = response.json()
            error = json_response.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                # 3. Use the access token to access the API
                access_token = json_response.get("access_token")
                # Get user profile
                response = requests.get(
                    settings.GITHUB_USERINFO_ENDPOINT,
                    headers={"Authorization": f"token {access_token}", "Accept": "application/json"},
                )
                json_response = response.json()
                userid = json_response.get("login", None)

                if userid is not None:
                    name = json_response.get("name")
                    email = json_response.get("email")
                    bio = json_response.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            # raise GithubException()
                            user.login_method = models.User.LOGIN_GITHUB
                            user.email_verified = True
                            user.verification_code = ""
                            user.save()
                    except models.User.DoesNotExist:
                        user = models.User.object.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()  # Marks the user as having no password set.
                        user.save()

                    login(request, user)
                    messages.success(request, f"Welcome, {user.first_name}!")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get user profile")
        else:
            raise GithubException("Something went wrong")

    except Exception as e:
        # TODO: error messages
        # messages.debug(request, "Something went wrong with client (%s)" % client_id)
        messages.error(request, e)
        return redirect(reverse("users:login"))


def google_login(request):
    # 1. Send an authentication request to Google
    client_id = settings.GOOGLE_ID
    redirect_uri = settings.GOOGLE_CALLBACK_URL
    return redirect(
        f"{settings.GOOGLE_AUTHORIZATION_ENDPOINT}"
        + f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=openid email profile"
    )


class GoogleException(Exception):
    pass


def google_callback(request):
    try:
        client_id = settings.GOOGLE_ID
        client_secret = settings.GOOGLE_SECRET
        redirect_uri = settings.GOOGLE_CALLBACK_URL
        # 2. Exchange code for access token and ID token
        code = request.GET.get("code", None)
        if code is not None:
            response = requests.post(
                settings.GOOGLE_TOKEN_ENDPOINT,
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
                headers={"Accept": "application/json"},
            )
            json_response = response.json()
            error = json_response.get("error", None)
            if error is not None:
                raise GoogleException("Can't get access token")
            else:
                access_token = json_response.get("access_token")
                # 3. Obtain user information from the ID token
                response = requests.get(f"{settings.GOOGLE_USERINFO_ENDPOINT}?access_token={access_token}&alt=json",)
                json_response = response.json()
                # id = json_response.get("id", None)
                sub = json_response.get("sub", None)

                # if id is not None:
                if sub is not None:
                    first_name = json_response.get("given_name")
                    last_name = json_response.get("family_name")
                    email = json_response.get("email")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GOOGLE:
                            # raise GoogleException()
                            user.login_method = models.User.LOGIN_GOOGLE
                            user.email_verified = True
                            user.verification_code = ""
                            user.save()
                    except models.User.DoesNotExist:
                        user = models.User.object.create(
                            username=email,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            login_method=models.User.LOGIN_GOOGLE,
                            email_verified=True,
                        )
                        user.set_unusable_password()  # Marks the user as having no password set.
                        user.save()

                    login(request, user)
                    messages.success(request, f"Welcome, {user.first_name}!")
                    return redirect(reverse("core:home"))
                else:
                    raise GoogleException("Can't get user profile")
        else:
            raise GoogleException("Something went wrong")

    except Exception as e:
        # TODO: error messages
        messages.error(request, e)
        return redirect(reverse("users:login"))


def facebook_login(request):
    # 1. Send an authentication request to Facebook
    client_id = settings.FACEBOOK_ID
    redirect_uri = settings.FACEBOOK_CALLBACK_URL
    state = "{st=state123abc,ds=123456789}"
    return redirect(
        f"{settings.FACEBOOK_AUTHORIZATION_ENDPOINT}"
        + f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}&scope=email"
    )


class FacebookException(Exception):
    pass


def facebook_callback(request):
    try:
        client_id = settings.FACEBOOK_ID
        client_secret = settings.FACEBOOK_SECRET
        redirect_uri = settings.FACEBOOK_CALLBACK_URL
        # 2. Exchange code for access token and ID token
        code = request.GET.get("code", None)
        print(f"code: {code}")
        if code is not None:
            response = requests.get(
                f"{settings.FACEBOOK_TOKEN_ENDPOINT}"
                + f"?client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}"
            )
            json_response = response.json()
            print(f"json response: {json_response}")
            error = json_response.get("error", None)
            if error is not None:
                raise FacebookException("Can't get access token")
            else:
                access_token = json_response.get("access_token")
                # 3. Obtain user information from the ID token
                response = requests.get(
                    f"{settings.FACEBOOK_USERINFO_ENDPOINT}"
                    + f"?fields=id,name,first_name,last_name,email&access_token={access_token}"
                )
                json_response = response.json()
                id = json_response.get("id", None)

                if id is not None:
                    first_name = json_response.get("first_name")
                    last_name = json_response.get("last_name")
                    email = json_response.get("email")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_FACEBOOK:
                            # raise FacebookException()
                            user.login_method = models.User.LOGIN_FACEBOOK
                            user.email_verified = True
                            user.verification_code = ""
                            user.save()
                    except models.User.DoesNotExist:
                        user = models.User.object.create(
                            username=email,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            login_method=models.User.LOGIN_FACEBOOK,
                            email_verified=True,
                        )
                        user.set_unusable_password()  # Marks the user as having no password set.
                        user.save()

                    login(request, user)
                    messages.success(request, f"Welcome, {user.first_name}!")
                    return redirect(reverse("core:home"))
                else:
                    raise FacebookException("Can't get user profile")
        else:
            raise FacebookException("Something went wrong")

    except Exception as e:
        # TODO: error messages
        messages.error(request, e)
        return redirect(reverse("users:login"))


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


class UserProfileView(DetailView):

    model = models.User

    # context_object_name: Designates the name of the variable to use in the context.
    # Here, default context_object_name is user.
    # But we are using user object for current logged in user.
    # So it make some problem when we access other user in template.
    # e.g. from this link <a href="{{room.host.get_absolute_url}}">
    # Set context_object_name here, so that we can distinguish selected user and authorized user.
    context_object_name = "user_selected"

    # How to extend context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extended_value"] = "This is an extended data to context!"  # use {{extended_value}} in templates
        return context


# Tips! trade-off with UpdateView
# If you want to have more customizable update view,
# Don't use UpdateView, but use FormView with ModelForm! (Preferred, if you have enough time to do)
# Using FormView is always preferred because using UpdateView and set widget is too hacky!
#
# With FormView for UpdateView, we would have to
# 1. create a form
# 2. recieve get requests
# 3. find a user
# 4. put user data inside of the form
# then, override form_valid(), save, redirect..
class UserProfileUpdateView(UpdateView):

    """ User Profile Update View
        https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-editing/#model-forms
        You don’t even need to provide a success_url for CreateView or UpdateView
        - they will use get_absolute_url() on the model object if available.
    """

    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        # "email",  # not allow to change username
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    # Overriding get_object()
    # http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/UpdateView/#get_object
    # Django automatically calls get_object() to get the object that needs to be updated by your form
    def get_object(self, queryset=None):
        # print(f"get_object: {self.request.user.avatar}")
        return self.request.user
        # e.g. return OtherModel.objects.get(pk=self.request.GET.get('pk'))

    # Overriding get_form()
    # http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/UpdateView/#get_form
    # To modify the current form
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        # print(form)  # to check fields name
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        return form

    # Overriding form_valid() - intercepting changes
    # http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/UpdateView/#form_valid
    def form_valid(self, form):
        # Applying email changes to username
        # 1. catch email before it's saved
        # 2. and copy it as username
        email = form.cleaned_data.get("email")
        if email is not None:
            self.object.username = email
            self.object.save()
        return super().form_valid(form)


class PasswordUpdateView(PasswordChangeView):

    template_name = "users/update_password.html"
    # success_url = reverse_lazy("core:home")  # go to home

    # Modify the current form
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        # print(form)  # to check fields name
        form.fields["old_password"].widget.attrs = {"placeholder": "Old password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "New password confirmation"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # go to profile
