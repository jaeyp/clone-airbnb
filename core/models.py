from django.db import models

# Create your models here.


class AbsctractTimeStampedModel(models.Model):

    """ Time Stamped Model
        This model deribes models.Model and extends it by adding TimeStamp features
        This model doesn't go to database
        This model will be used to craete other models which will go to database

        To save create & update time for a class object
    """

    # auto_now_add=True
    # Automatically set the field to now when the object is first created.
    created = models.DateTimeField(auto_now_add=True)
    # auto_now=True
    # Automatically set the field to now every time the object is saved.
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This is an abstract model to extend other models
