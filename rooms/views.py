from django.utils import timezone

# Function Based Views in manual way
# from math import ceil

# Function Based Views with Paginator
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage

# Class Based Views
from django.views.generic import ListView

from . import models

# Create your views here.


class HomeView(ListView):

    """ HomeView Definition
        Class Based View
    """

    # 1. Set HomeView.model or HomeView.queryset
    model = models.Room

    # 2. Set Attributes: check ccbv.co.uk
    paginate_by = 5
    paginate_orphans = 2
    ordering = "price"
    page_kwarg = "page"  # page keyward argument - default: "page"
    # context_object_name = "rooms"  # change object_list to rooms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context

    # Use page_obj in order to access a page instance in template


def all_rooms(request):
    """ all_rooms
        Function Based View
        it renders home.html page by using Paginator
        https://docs.djangoproject.com/en/2.2/topics/pagination/
    """
    # 1. Get the value of key "page" from GET request
    page = request.GET.get("page", 1)

    # 2. Get a QuerySet of Room
    all_rooms = models.Room.objects.all()

    # 3. Create a Paginator instance
    paginator = Paginator(all_rooms, 5, orphans=2)
    # print(vars(rooms))  # object_list of rooms in the page, number, paginator instance
    # print(vars(rooms.paginator))  # object_list of all room, per_page, orphans, allow_empty_first_page, count, num_pages

    # 4-1. Create a Page object using get_page()
    """ get_page()
        it returns the first page if the page number is negative,
        or
        it returns the last page if the page greater than the number of pages.
    """
    # rooms = paginator.get_page(page)  # rooms is a Page object: Paginator.page()

    # 4-2. Create a Page object using page()
    """ page()
        it raises InvalidPage if the given page number doesn’t exist.
    """
    # 4-2-1. returns the first page if no objects exist on that page.
    """
    try:
        rooms = paginator.page(int(page))
    except EmptyPage:
        rooms = paginator.page(1)

    return render(request, "rooms/home.html", {"use_paginator": True, "page": rooms})
    """

    # 4-2-2. redirect to home page if no objects exist on that page.
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"use_paginator": True, "page": rooms})
    except EmptyPage:
        rooms = paginator.page(int(1))
        return render(request, "rooms/home.html", {"use_paginator": True, "page": rooms})
    except Exception:
        return redirect("/")


""" manual navigator
def all_rooms(request):
    # if "page" doesn't exist, set 1
    page = request.GET.get("page", 1)
    # if the value of "page" is empty, set 1
    page = int(page or 1)
    page_size = 5
    limit = page_size * page
    offset = limit - page_size

    # Limiting QuerySets
    #    Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results.
    #    This is the equivalent of SQL’s LIMIT and OFFSET clauses.
    all_rooms = models.Room.objects.all()[offset:limit]
    total_page = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={"rooms": all_rooms, "page": page, "total_page": total_page, "page_range": range(1, total_page + 1)},
    )
"""
