import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# support sending email
from django.conf import settings  # To access environment variables from config/settings.py
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


# Create your models here.

""" Tips.
    If you cannot go to definition of a parent django class (AbstractUser),
    Set Python: Select Interpreter (for this, choose 'airbnb':pipenv)
"""


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"), (GENDER_OTHER, "Other"))

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_CAD = "cad"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_CAD, "CAD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_FACEBOOK = "facebook"
    LOGIN_GOOGLE = "google"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_FACEBOOK, "Facebook"),
        (LOGIN_GOOGLE, "Google"),
    )

    # [null vs blank]
    # null is purely database-related (for DB), whereas blank is validation-related (for Form)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, null=True, blank=True, default=LANGUAGE_ENGLISH)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, null=True, blank=True, default=CURRENCY_CAD)
    superhost = models.BooleanField(default=False)  # certified host user by Airbnb
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(
        max_length=120, default="", blank=True
    )  # random secret code for email varification
    login_method = models.CharField(choices=LOGIN_CHOICES, max_length=20, null=True, blank=True, default=LOGIN_EMAIL)

    def verify_email(self):
        if self.email_verified is False:
            # generate random number
            verification_code = uuid.uuid4().hex[:6]
            self.verification_code = verification_code

            # send mail
            print(f"EMAIL_HOST_USER:{settings.EMAIL_HOST_USER}")
            print(f"SEND EMAIL for VERIFICATION with {verification_code} from {settings.EMAIL_FROM} to {self.email}")
            html_message = render_to_string(
                "emails/verify_email.html",
                {
                    "verification_callback_url": settings.VERIFICATION_CALLBACK_URL,
                    "verification_code": verification_code,
                },
            )
            # html_message = (
            #     "To verify your email, click "
            #     + "<a href='{http://127.0.0.1:8000/users/verify/}{verification_code}'>here</a>"
            # )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),  # it removes all the html tags except for plain text.
                # f"Verify account, this is your verification code: {verification_code}",
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
