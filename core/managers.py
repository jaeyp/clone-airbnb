from django.db import models


class CustomModelManager(models.Manager):
    """ Custom managers - extending default manager (models.Manager)
        https://docs.djangoproject.com/en/2.2/topics/db/managers/#custom-managers
    """

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
