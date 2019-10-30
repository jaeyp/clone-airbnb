from django.shortcuts import render
from . import models

# Create your views here.


def all_rooms(request):
    """ Limiting QuerySets
        Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results.
        This is the equivalent of SQL’s LIMIT and OFFSET clauses.
    """
    all_rooms = models.Room.objects.all()[:10]
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
