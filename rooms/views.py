from math import ceil
from django.shortcuts import render
from . import models

# Create your views here.


def all_rooms(request):
    """
        print(request.GET)
        print(request.GET.keys())
        # var() returns the __dict__ attributes for any object.
        # var() acts like locals() method when an empty argument is passed.
        # locals() returns the dictionary of current local symbol table.
        print(vars(request.GET))
        # dir() returns list of the attributes and methods of any object.
        print(dir(request.GET))
    """
    # if "page" doesn't exist, set 1
    page = request.GET.get("page", 1)
    # if the value of "page" is empty, set 1
    page = int(page or 1)
    page_size = 5
    limit = page_size * page
    offset = limit - page_size

    """ Limiting QuerySets
        Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results.
        This is the equivalent of SQL’s LIMIT and OFFSET clauses.
    """
    all_rooms = models.Room.objects.all()[offset:limit]
    total_page = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={"rooms": all_rooms, "page": page, "total_page": total_page, "page_range": range(1, total_page + 1)},
    )
