from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AbsctractTimeStampedModel

# Create your models here.


class Review(AbsctractTimeStampedModel):

    """ Review Model Definition """

    RATE_1 = 1
    RATE_2 = 2
    RATE_3 = 3
    RATE_4 = 4
    RATE_5 = 5
    # TODO: declined (by host), accepted (instead of confirmed)

    # Check Model.get_FOO_display()
    # https://docs.djangoproject.com/en/2.2/ref/models/instances/#extra-instance-methods
    RATE_CHOICES = (
        (RATE_1, 1),
        (RATE_2, 2),
        (RATE_3, 3),
        (RATE_4, 4),
        (RATE_5, 5),
    )

    review = models.TextField()

    """ validators
        https://docs.djangoproject.com/en/2.2/ref/validators/
        You should validate field in forms, but also validate it in models
        because 'min_value' and 'max_value' arguments here gives you front-end side validation
        while 'validators=[MinValueValidator(1), MaxValueValidator(5)]' in models gives you back-end side validation.

        In this case, we don't need to set validators here since we set 'choices=RATE_CHOICES'
    """
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATE_CHOICES, default=RATE_3
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATE_CHOICES, default=RATE_3
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATE_CHOICES, default=RATE_3
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATE_CHOICES, default=RATE_3
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATE_CHOICES, default=RATE_3
    )
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATE_CHOICES, default=RATE_3
    )

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

    class Meta:
        ordering = ("-created",)  # ordering review data
