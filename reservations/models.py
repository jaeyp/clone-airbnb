import datetime
from django.db import models
from util import debug

""" Tips.
    We use django.utils for timezone instead of python.utils
    in order to keep this server TIME_ZONE in config/settings.py
"""
from django.utils import timezone
from core.models import AbsctractTimeStampedModel

# from . import manager  # moved to core/managers.py

# Create your models here.


class BookedDay(AbsctractTimeStampedModel):

    day = models.DateField()
    # Each booked day refer to a specific reservation
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    # Model Meta options: https://docs.djangoproject.com/en/2.2/ref/models/options/
    class Meta:
        # verbose_name: A human-readable name for the object, singular
        # If this isn’t given, Django will use a munged version of the class name: CamelCase becomes camel case.
        verbose_name = "Booked Day"
        # verbose_name_plural: The plural name for the object:
        # If this isn’t given, Django will use verbose_name + "s".
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


class Reservation(AbsctractTimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"  # by guest
    # TODO: declined (by host), accepted (instead of confirmed)

    # Check Model.get_FOO_display()
    # https://docs.djangoproject.com/en/2.2/ref/models/instances/#extra-instance-methods
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    check_in = models.DateField()
    check_out = models.DateField()
    # Tips. ForeignKey.related_name
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey.related_name
    # it allows for the related object to refer to this object. like "self.reservations.all()" in rooms/models
    guest = models.ForeignKey("users.User", related_name="reservations", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", related_name="reservations", on_delete=models.CASCADE)

    # Change default Mnanger (models.Manager to CustomModelManager)
    # objects = managers.CustomModelManager()  # moved to core/managers.py

    class Meta:
        ordering = ["check_in"]

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True  # this display x/o icon in admin page intead of False/True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            # schedule is done, delete related booked days
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True  # this display x/o icon in admin page intead of False/True

    def save(self, *args, **kwargs):
        """ Overriding save()
            To create new booked days only when new reservation is created.
        """
        if self.pk is None:  # for a new reservation
            # create new booked days
            start = self.check_in
            end = self.check_out
            difference = end - start  # datetime difference!  it's not an integer!
            existing_booked_day = (
                BookedDay.objects.filter(reservation__room=(self.room))
                .filter(
                    # In Django Model QuerySet Objects, Double Underscore ( __ ) Means "Field Lookups".
                    # day__range: field-name__lookup-type-keywordm"
                    # Simply, just replace and think "__" is "`s" in any situations in Django
                    # like day__range=(start, end): day's range is between start and end
                    day__range=(start, end)  # day__range: find BookedDay.day between start and end
                )
                .exists()
            )  # if BookedDay exists between start & end day or not

            if existing_booked_day is False:
                # First, Save a new Reservation
                super().save(*args, **kwargs)

                # Then, Create a new BookedDay for the Reservation
                for i in range(difference.days):
                    day = start + datetime.timedelta(days=i)
                    debug.info(f"{day} booked")
                    # According to relation, BookedDay wouldn't be able to be created if reservation wasn't saved
                    BookedDay.objects.create(day=day, reservation=self)
            else:
                print(f"booked day is existing between {start} and {end}")
        else:  # for an existing reservation
            # do as usual
            return super().save(*args, **kwargs)
