from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),  # {% url 'users:login' %}
    path("logout/", views.log_out, name="logout"),  # users:logout
    path("signup/", views.SignUpView.as_view(), name="signup"),  # users:signup
    path("verify/<str:key>/", views.complete_verification, name="complete-verification"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),  # {% url 'users:profile' user.pk %}
    path("update-profile/", views.UserProfileUpdateView.as_view(), name="update"),
    path("update-password/", views.PasswordUpdateView.as_view(), name="password"),
    path("switch-hosting/", views.switch_hosting, name="switch-hosting"),
    # TODO: integrate three social logins (github, google, facebook)
    # path("login/social/<str:key>", views.social_login, name="social-login"),
    path("login/github/", views.github_login, name="github-login"),  # users:github-login
    path("auth/github/", views.github_callback, name="github-callback"),
    path("login/google/", views.google_login, name="google-login"),  # users:google-login
    path("auth/google/", views.google_callback, name="google-callback"),
    path("login/facebook/", views.facebook_login, name="facebook-login"),  # users:facebook-login
    path("auth/facebook/", views.facebook_callback, name="facebook-callback"),
]
