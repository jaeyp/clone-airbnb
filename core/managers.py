from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):  # for other models except for User model
    """ Custom managers - extending default manager (models.Manager)
        https://docs.djangoproject.com/en/2.2/topics/db/managers/#custom-managers
    """

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomUserManager(CustomModelManager, UserManager):  # for User model in order to support create_superuser()
    pass

