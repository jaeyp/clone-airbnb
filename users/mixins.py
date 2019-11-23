from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin

# https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin


class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found"

    # if test_func return Ture, it go ahead.
    def test_func(self):
        return not self.request.user.is_authenticated

    # https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.mixins.AccessMixin.handle_no_permission
    def handle_no_permission(self):
        return redirect("core:home")
