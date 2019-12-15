# 1. import python packages
# e.g. import os
import uuid

# 2. import django packages
from django.db import models
from django.urls import reverse
from django.utils import timezone

# 3. import third-party packages
from django_countries.fields import CountryField

# 4. import project own packages
from core.models import AbsctractTimeStampedModel
from users.models import User
from util.cal import Calendar

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
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
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

    # ======================================
    # OVERRIDING PREDEFINED MODEL METHODS
    # ======================================

    def __str__(self):
        return self.name

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

        """ Overriding save method """

        # Do something required before saving
        self.city = str.capitalize(self.city)

        # then, save it
        super().save(*args, **kwargs)  # Call the actual save() method
        # super(ModelName, self).save(*args, **kwargs)

        # Do something required after saving here.

    def get_absolute_url(self):

        """ Overriding get_absolute_url method 
            https://docs.djangoproject.com/en/2.2/ref/models/instances/#get-absolute-url

            Define a get_absolute_url() method to tell Django how to calculate the canonical URL for an object.
            To callers, this method should appear to return a string that can be used to refer to the object over HTTP.

            One place Django uses get_absolute_url() is in the admin app. 
            If an object defines this method, the object-editing page will have a “View on site” link
            that will jump you directly to the object’s public view, as given by get_absolute_url().
        """

        """ reverse()
            https://docs.djangoproject.com/en/2.2/ref/urlresolvers/#reverse
            
            you can convert URL_pattern_name to absolute_url
            e.g.
            if you have 'detail' url pattern in rooms/urls.py like this,
                urlpatterns = [path("<int:id>", views.room_detail, name="detail")]
            you can invoke reverse() like this,
                reverse("rooms:detail", kwargs={"id": self.id})
        """
        return reverse("rooms:detail", kwargs={"pk": self.pk})  # rooms:detail + id => /room/id

    # ======================================
    # CUSTOM METHODS
    # ======================================

    def get_total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0

        for review in all_reviews:
            all_ratings += review.rating_average()

        if len(all_reviews) > 0:
            return round(all_ratings / len(all_reviews), 2)
        else:
            return 0

    def get_first_photo(self):

        """ Get the first photo of room """

        # Unpacking (destructuring) assignment
        # Put comma (photo,) in order to let python know we want to get the first eliment of array
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):

        """ Get the first five photos of room """
        try:
            photos = self.photos.all()[1:5]
            print(photos)
            return photos
        except ValueError:
            return None

    def get_all_photos(self):

        """ Get all photos of room """
        try:
            photos = self.photos.all()
            return photos
        except ValueError:
            return None

    def get_first_two_reviews(self):

        reviews = self.reviews.all()[:2]
        print(reviews)
        return reviews

    def get_next_two_reviews(self):

        reviews = self.reviews.all()[2:4]
        return reviews

    def get_reservations(self):

        reservations = self.reservations.all()
        # print(list(reservations))
        return reservations

    def get_calendars(self):
        now = timezone.now()
        # calculate next month
        next_year = this_year = now.year
        this_month = now.month
        next_month = this_month % 12 + 1
        if next_month == 1:
            next_year = this_year + 1
        # or use deltatime

        this_month_cal = Calendar(this_year, this_month, self.pk)
        next_month_cal = Calendar(next_year, next_month, self.pk)
        return [this_month_cal, next_month_cal]

    # It's deprecated by prularize
    # https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#pluralize
    #
    # def get_guests(self):
    #     if self.guests == 1:
    #         return "1 guest"
    #     else:
    #         return f"{self.guests} guests"
    # def get_beds(self):
    #     if self.beds == 1:
    #         return "1 bed"
    #     else:
    #         return f"{self.beds} beds"
    # def get_bedrooms(self):
    #     if self.bedrooms == 1:
    #         return "1 bedroom"
    #     else:
    #         return f"{self.bedrooms} bedrooms"
    # def get_bathrooms(self):
    #     if self.bathrooms == 1:
    #         return "1 bathroom"
    #     else:
    #         return f"{self.bathrooms} bathrooms"


# image upload to dynamic path
def get_upload_to(instance, filename):
    new_filename = "{}.{}".format(uuid.uuid1(), filename.split(".")[-1])
    return "room_photos/{}/{}".format(instance.room.pk, new_filename)


class Photo(AbsctractTimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to=get_upload_to)  # path: /uploads/room_photos
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption
