"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.contrib.messages import constants as message_constants  # messages
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "(3up+$)ymc!pjiq1!(4(@xm@jba(v0_ds$8zq+hw3xthg6k%4f"
# DJANGO_SECRET for production and the second key for dev version
SECRET_KEY = os.environ.get("DJANGO_SECRET", "8^6$fZANh9yX2!tYG27te%DxcQSmXgpJ")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# ALLOWED_HOSTS = "*"

DEBUG = bool(os.environ.get("DEBUG"))  # this will be False on AWS EB server since there is no .env file on EB machine
# DEBUG = True  # To debug having more information in yellow page with HTTP error
# print(type(DEBUG))

# Default Message Level : INFO (20)
# https://docs.djangoproject.com/en/2.2/ref/contrib/messages/#message-levels
MESSAGE_LEVEL = message_constants.DEBUG  # 10

# Route53 DNS for EB production
ROUTE53_DNS = os.environ.get("ROUTE53_DNS", "localhost:8000")

# if DEBUG is False:  # To debug having more information in yellow page with HTTP error
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "192.168.2.22"]
else:
    ALLOWED_HOSTS = [".elasticbeanstalk.com", ROUTE53_DNS]
    # ALLOWED_HOSTS = [".elasticbeanstalk.com", "airbnb-clone.jaeyp.xyz"]

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["django_countries", "django_seed", "import_export", "storages"]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "reviews.apps.ReviewsConfig",
    "reservations.apps.ReservationsConfig",
    "lists.apps.ListsConfig",
    "conversations.apps.ConversationsConfig",
]

CUSTOM_TAGS = [
    "rooms.templatetags.room_extras",
    "users.templatetags.user_filters",
    "reservations.templatetags.math_filters",
    "reservations.templatetags.date_filters",
]  # rooms/templatetags/room_extras.py

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS + CUSTOM_TAGS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#how-django-discovers-language-preference
    "django.middleware.locale.LocaleMiddleware",
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

# if DEBUG is False:  # To debug having more information in yellow page with HTTP error
if DEBUG:  # for Development
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}
else:  # for AWS EB
    DATABASES = {
        "default": {
            # RDS info: https://ca-central-1.console.aws.amazon.com/rds/home?region=ca-central-1#database:id=airbnb-clone;is-cluster=false
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.environ.get("RDS_HOST"),  # Endpoint
            "NAME": os.environ.get("RDS_NAME"),  # DB identifier
            "USER": os.environ.get("RDS_USER"),  # Master username
            "PASSWORD": os.environ.get("RDS_PASSWORD"),
            "PORT": os.environ.get("RDS_PORT"),
        }
    }


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

STATIC_URL = "/static/"  # jaey. this 'static' is a url path

# jaey. set static file directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]  # jaey. this 'static' is a project directory name for static files

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
# EMAIL_FROM = "noreply@" + os.environ.get("MAILGUN_DOMAIN")
# TODO: adding evironment properties in AWS EB
# This occurs error with "eb deploy". (TypeError: must be str, not NoneType)
# because .env is NOT commited into git repository.
EMAIL_FROM = "noreply@jaeyp.xyz"

# User Verification Callback URL
# TODO: support production url from EB property instead of localhost:8000
# VERIFICATION_CALLBACK_URL = "http://127.0.0.1:8000/users/verify"
VERIFICATION_CALLBACK_URL = f"http://{ROUTE53_DNS}/users/verify"

# Social Login - Github
GITHUB_ID = os.environ.get("GITHUB_ID")
GITHUB_SECRET = os.environ.get("GITHUB_SECRET")
# TODO: support production url from EB property instead of localhost:8000
# GITHUB_CALLBACK_URL = os.environ.get("GITHUB_CALLBACK_URL", "http://localhost:8000/users/auth/github")
GITHUB_CALLBACK_URL = f"http://{ROUTE53_DNS}/users/auth/github"
# print(f"GITHUB_CALLBACK_URL: {GITHUB_CALLBACK_URL}")
# Ref. Authorizing OAuth Apps
# https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
GITHUB_AUTHORIZATION_ENDPOINT = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"
GITHUB_USERINFO_ENDPOINT = "https://api.github.com/user"

# Social Login - Google
GOOGLE_ID = os.environ.get("GOOGLE_ID")
GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET")
# TODO: support production url from EB property instead of localhost:8000
# GOOGLE_CALLBACK_URL = os.environ.get("GOOGLE_CALLBACK_URL", "http://localhost:8000/users/auth/google")
GOOGLE_CALLBACK_URL = f"http://{ROUTE53_DNS}/users/auth/google"
# Ref. OpenID Connect
# https://developers.google.com/identity/protocols/OpenIDConnect
# Ref. Endpoints for OpenID Connect
# https://developers.google.com/identity/protocols/OpenIDConnect#discovery
# GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/auth?"
GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
# GOOGLE_TOKEN_ENDPOINT = "https://accounts.google.com/o/oauth2/token"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
# GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"

# Social Login - Facebook
FACEBOOK_ID = os.environ.get("FACEBOOK_ID")
FACEBOOK_SECRET = os.environ.get("FACEBOOK_SECRET")
# TODO: support production url from EB property instead of localhost:8000
# FACEBOOK_CALLBACK_URL = os.environ.get("FACEBOOK_CALLBACK_URL", "http://localhost:8000/users/auth/facebook")
FACEBOOK_CALLBACK_URL = f"http://{ROUTE53_DNS}/users/auth/facebook"
# Ref. Manually Build a Login Flow
# https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/
FACEBOOK_AUTHORIZATION_ENDPOINT = "https://www.facebook.com/v5.0/dialog/oauth"
# Ref. Access Tokens
# https://developers.facebook.com/docs/facebook-login/access-tokens/
FACEBOOK_TOKEN_ENDPOINT = "https://graph.facebook.com/v5.0/oauth/access_token"
# Ref. Retrieve User Profile via the Graph API
# https://developers.facebook.com/docs/php/howto/example_retrieve_user_profile/
# Ref. Graph API - User
# https://developers.facebook.com/docs/graph-api/reference/user/
FACEBOOK_USERINFO_ENDPOINT = "https://graph.facebook.com/me"


# To support login_required decorator
# https://docs.djangoproject.com/en/2.2/topics/auth/default/#the-login-required-decorator
LOGIN_URL = "/users/login"


# Locale
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


# for EB deployment
if not DEBUG:
    # django-storages
    # DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # separating uploads folder from static folder (static/uploads/ -> stitic/ and uploads/)
    DEFAULT_FILE_STORAGE = "config.custom_storages.UploadStorage"
    STATICFILES_STORAGE = "config.custom_storages.StaticStorage"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = (
        "airbnb-clone-eb"  # TODO: you should set very random difficult bucket name for this for security
    )
    AWS_AUTO_CREATE_BUCKET = True
    AWS_BUCKET_ACL = "public-read"  # allow everybody to read files
    # https://airbnb-clone-eb.s3.amazonaws.com/img/logo.svg
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    # override static and media file path
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

    # Sentry
    sentry_sdk.init(dsn=os.environ.get("SENTRY_URL"), integrations=[DjangoIntegration()], send_default_pii=True)
else:  # for testing if 'django-admin collectstatic' command works
    # django-storages
    """ Enable this only for testing
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = (
        "airbnb-clone-eb"  # TODO: you should set very random difficult bucket name for this for security
    )
    AWS_AUTO_CREATE_BUCKET = True
    AWS_BUCKET_ACL = "public-read"  # allow everybody to read files """


# EB Django Superuser
SU_USERNAME = os.environ.get("SU_USERNAME")
SU_EMAIL = os.environ.get("SU_EMAIL")
SU_PASSWORD = os.environ.get("SU_PASSWORD")
