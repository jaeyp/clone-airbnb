from django.db import models
from core.models import AbsctractTimeStampedModel

# Create your models here.


class WishList(AbsctractTimeStampedModel):

    """ WishList Model Definition """

    name = models.CharField(max_length=80)

    # One to Many relation: an user can have many lists
    """ If you want to allow only one list for an user,
        Use OneToOneField() instead of ForeignKey() """
    user = models.ForeignKey("users.User", related_name="wishlists", on_delete=models.CASCADE)

    rooms = models.ManyToManyField("rooms.Room", related_name="wishlists", blank=True)

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "Number of Rooms"
