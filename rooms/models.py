# 1. import python packages
# e.g. import os
# 2. import django packages
from django.db import models

# 3. import third-party packages
from django_countries.fields import CountryField

# 4. import project own packages
from core.models import AbsctractTimeStampedModel
from users.models import User

# Create your models here.


class AbstractItem(AbsctractTimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    # Model Meta options: https://docs.djangoproject.com/en/2.2/ref/models/options/
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PropertyType(AbstractItem):

    """ PropertyType Model Definition """

    class Meta:
        verbose_name = "Property type"
        ordering = ["name"]  # ['-created']: decending order with '-' by created time


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House rule"


class Room(AbsctractTimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instance_book = models.BooleanField(default=False)
    # plus = models.BooleanField(default=False)  # verified room by Airbnb for quality and design

    # Sets ForeignKey having many to one relationship with User
    """ on_delete=models.CASCADE
        Cascade deletes. Django emulates the behavior of the SQL constraint ON DELETE CASCADE
        and also deletes the object containing the ForeignKey.
        This allow to create a recursive relationship with a specific User
    """
    # related_name: set alias for QuerySet 'room_set'.
    # Don't forget related_name is for target object_set (e.g. rooms for this class)
    host = models.ForeignKey(User, related_name="rooms", on_delete=models.CASCADE)  # connecting Room to User
    property_type = models.ForeignKey(PropertyType, related_name="rooms", on_delete=models.SET_NULL, null=True)

    # Sets many to many relationship between Room and Amenities
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    # Overriding __str__ method
    def __str__(self):
        return self.name

    # Overriding predefined model methods
    """
        In particular you’ll often want to change the way save() and delete() work.

        def save(self, *args, **kwargs):
            if prevent_condition:
                return
            else:
                do_something()
                super().save(*args, **kwargs)  # Call the "real" save() method.
                do_something_else()
    """

    def save(self, *args, **kwargs):

        """
            args: arguments
            kwargs: keyword arguments
        """

        # do something
        self.city = str.capitalize(self.city)

        super().save(*args, **kwargs)  # Call the real save() method
        # super(ModelName, self).save(*args, **kwargs)  # Call the real save() method

        # do something else

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0

        for review in all_reviews:
            all_ratings += review.rating_average()

        if len(all_reviews) > 0:
            return round(all_ratings / len(all_reviews), 2)
        else:
            return 0


class Photo(AbsctractTimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption
