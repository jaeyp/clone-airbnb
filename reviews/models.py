from django.db import models
from core.models import AbsctractTimeStampedModel

# Create your models here.


class Review(AbsctractTimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    # Tips. ForeignKey.related_name
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey.related_name
    # it allows for the related object to refer to this object. like "self.reviews.all()" in rooms/models
    user = models.ForeignKey("users.User", related_name="reviews", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", related_name="reviews", on_delete=models.CASCADE)
    # TODO: adding review date => use 'created'
    # AbsctractTimeStampedModel has 'created' attribute.

    def __str__(self):
        return f"{self.review} - {self.room}"

    """ Tips.
        Define methods in models.py if it should be invoked everywhere, user, admin...
    """

    def rating_average(self):
        avg = (self.accuracy + self.communication + self.cleanliness + self.location + self.check_in + self.value) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."
