from django.contrib.auth.models import AbstractUser
from django.db import models

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

    # [null vs blank]
    # null is purely database-related (for DB), whereas blank is validation-related (for Form)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, null=True, blank=True, default=LANGUAGE_ENGLISH)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, null=True, blank=True, default=CURRENCY_CAD)
    superhost = models.BooleanField(default=False)  # certified host user by Airbnb
    email_confirmed = models.BooleanField(default=False)
