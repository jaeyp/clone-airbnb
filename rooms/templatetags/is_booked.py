import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()

# Writing custom template tags
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#simple-tags
# @register.simple_tag(takes_context=True)


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        # In Django Model QuerySet Objects, Double Underscore ( __ ) Means "Field Lookups".
        # reservation__room: field-name__lookup-type-keyword
        # So, .get(reservation__room=my_room) means "look up reservations in room is my_room"
        # Simply, just replace and think "__" is "`s" in any situations in Django
        # like reservation__room=my_room: reservation's room is my_room
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True  # day is booked
    except reservation_models.BookedDay.DoesNotExist:
        return False  # day is not booked yet
