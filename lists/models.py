from django.db import models
from core.models import AbsctractTimeStampedModel

# Create your models here.


class List(AbsctractTimeStampedModel):

    """ List Model Definition """

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", related_name="lists", on_delete=models.CASCADE)
    rooms = models.ManyToManyField("rooms.Room", related_name="lists", blank=True)

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "Number of Rooms"
