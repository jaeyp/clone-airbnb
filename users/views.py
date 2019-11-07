from django.views import View
from django.shortcuts import render
from . import forms

# Create your views here.


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
        return render(request, "users/login.html", {"form": form})
