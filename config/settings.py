"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "(3up+$)ymc!pjiq1!(4(@xm@jba(v0_ds$8zq+hw3xthg6k%4f"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# ALLOWED_HOSTS = "*"

DEBUG = True

ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["django_countries", "django_seed", "import_export"]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "reviews.apps.ReviewsConfig",
    "reservations.apps.ReservationsConfig",
    "lists.apps.ListsConfig",
    "conversations.apps.ConversationsConfig",
]

CUSTOM_TAGS = ["rooms.templatetags.room_extras"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS + CUSTOM_TAGS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"


# [Substituting a custom User model]
# It’s highly recommended to set up a custom user model, even if the default User model is
# sufficient for you. You’ll be able to customize it in the future if the need arises
AUTH_USER_MODEL = "users.User"

# Media files (images)
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# slash at first (root path) and last (required: It must end in a slash if set to a non-empty value)
MEDIA_URL = "/media/"


# Email Configuration
# https://app.mailgun.com/app/sending/domains/sandbox6e7e5be91a774358b8dc111d98d2e4f1.mailgun.org/credentials
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = "587"  # 587: TLS, 465: SSL, 25: SMTP
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")
# with this given domain by mailgun, mail would go to the spam folder
EMAIL_FROM = "noreply@" + os.environ.get("MAILGUN_DOMAIN")

# User Verification Callback URL
VERIFICATION_CALLBACK_URL = "http://127.0.0.1:8000/users/verify"

# Social Login - Github
GITHUB_ID = os.environ.get("GITHUB_ID")
GITHUB_SECRET = os.environ.get("GITHUB_SECRET")
GITHUB_CALLBACK_URL = "http://localhost:8000/users/auth/github"
GITHUB_AUTHORIZATION_ENDPOINT = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"
GITHUB_USERINFO_ENDPOINT = "https://api.github.com/user"

# Social Login - Google
GOOGLE_ID = os.environ.get("GOOGLE_ID")
GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET")
GOOGLE_CALLBACK_URL = "http://localhost:8000/users/auth/google"
# Ref. https://developers.google.com/identity/protocols/OpenIDConnect#discovery
GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"

# Social Login - Facebook
FACEBOOK_ID = os.environ.get("FACEBOOK_ID")
FACEBOOK_SECRET = os.environ.get("FACEBOOK_SECRET")
FACEBOOK_CALLBACK_URL = "http://localhost:8000/users/auth/facebook"
