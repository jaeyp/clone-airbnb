import uuid

# gettext_lazy(): using lazy execution for translation
# https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#standard-translation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# support sending email
from django.conf import settings  # To access environment variables from config/settings.py
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from core import managers as core_managers


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

    GENDER_CHOICES = (
        ("", _("Select gender")),
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = (("", "Select language"), (LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_CAD = "cad"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (("", "Select currency"), (CURRENCY_USD, "USD"), (CURRENCY_CAD, "CAD"), (CURRENCY_KRW, "KRW"))

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
    avatar = models.ImageField(
        _("avatar"), upload_to="avatars", default="", null=True, blank=True
    )  # path: /uploads/avatars
    gender = models.CharField(_("gender"), choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    bio = models.TextField(_("bio"), default="", blank=True)
    birthdate = models.DateField(_("birthdate"), null=True, blank=True)
    language = models.CharField(
        _("language"), choices=LANGUAGE_CHOICES, max_length=2, null=True, blank=True, default=LANGUAGE_ENGLISH
    )
    currency = models.CharField(
        _("currency"), choices=CURRENCY_CHOICES, max_length=3, null=True, blank=True, default=CURRENCY_CAD
    )
    # TODO: does we need host field? or we just assume that user having room listing is a host?
    # host = models.BooleanField(default=False)  # host user
    superhost = models.BooleanField(_("superhost"), default=False)  # certified host user by Airbnb
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(
        max_length=120, default="", blank=True
    )  # random secret code for email varification
    login_method = models.CharField(
        _("login method"), choices=LOGIN_CHOICES, max_length=20, null=True, blank=True, default=LOGIN_EMAIL
    )

    # Change default Mnanger for having get_or_none() (models.Manager to core.managers.CustomModelManager)\
    """ TODO: bug-fix: creating a new user occurs error ('CustomModelManager' object has no attribute 'normalize_email')
    objects = core_managers.CustomModelManager()
    """

    def get_absolute_url(self):
        # print(f"users:profile with {self.pk}")
        return reverse("users:profile", kwargs={"pk": self.pk})

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
