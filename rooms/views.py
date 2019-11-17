from django.utils import timezone
from django.urls import reverse
from django.http import Http404

# Function Based Views in manual way
# from math import ceil

# Function Based Views with Paginator
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage

# Class Based Views
from django.views.generic import ListView, DetailView, View

# third-party packages
from django_countries import countries

# Custom packages
from . import models, forms

# Create your views here.


class HomeView(ListView):

    """ HomeView Definition
        Class Based Home View

        [Generic ListView]
        http://ccbv.co.uk/projects/Django/2.2/django.views.generic.list/ListView/
    """

    # 1. Set HomeView.model or HomeView.queryset
    model = models.Room

    # 2. Set Attributes: refers to ccbv.co.uk
    paginate_by = 5
    paginate_orphans = 2
    ordering = "price"
    # page_kwarg = "page"  # page keyward argument - default: "page"
    # context_object_name = "rooms"  # change object_list to rooms

    """ if you don't want to use the given template name from CBV,
        set template_name as an argument of as_view(), or inside HomeView class
    """
    # template_name = "rooms/home4cbv.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context

    # Use page_obj in order to access a page instance in template


def all_rooms(request):
    """ all_rooms
        Function Based Home View
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
    # print(vars(rooms.paginator))  # object_list of all room, per_page, orphans, allow_empty_first_page, count...

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


class RoomDetailView(DetailView):
    """ RoomDetailView definition
        Class Based Room Detail View

        [Generic DetailView]
        With DetailView, Django looks 'pk' url argument by default.
        http://ccbv.co.uk/projects/Django/2.2/django.views.generic.detail/DetailView/
    """

    model = models.Room
    pk_url_kwarg = "id"


def room_detail(request, id):
    """ room_detail
        Function Based Room Detail View
    """
    support_404 = True
    """ Custom 404 page
        In order to enable custom 404 page,
        you should change DEBUG setting from config/settings.py

        e.g.
        DEBUG = False
        ALLOWED_HOSTS = "*"
    """
    try:
        room = models.Room.objects.get(id=id)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        """ DoesNotExist is different from PageNotFound error of HTTP
            So, if we doesn't catch this error type,
            it will raise server error (500).
        """
        if support_404:
            """ Raise 404 error
                if you raise Http404(), django try to find & render 404.html from templates directory
            """
            raise Http404()
        else:
            # return redirect("")
            # return redirect("/")
            """ Tips.
                Always try to use reverse() instead of url as much as you can!
                It will help you a lot!
            """
            return redirect(reverse("core:home"))


class SearchView(View):
    """ SearchView definition
        Class Based Room Search View
        """

    def get(self, request):
        print(f"request: {request.GET}")  # get request with city - input name "city" from nav.html
        # TODO: - Rebuild Search Algorithm -
        # TODO: change input parameter name to "keyword" or "region" for accepting other types of search keyword
        #       e.g. city, country, more small area, Stays, Restaurants...
        # TODO: deduce a country code from input city
        # TODO: auto completion with city (e.g. "Seoul, South Korea" when tpye just "Seoul")
        # TODO: auto completion list while it's typing
        # TODO: search by Stays, Experiences, Restaurants
        country = request.GET.get("country")
        if country:
            print(f"there's a country: {country}")
            # How to pass request data into form:
            # Just By passing request.GET, we can store user requests!
            form = forms.SearchForm(request.GET)  # Bounded form
            # print(f"REQUEST: {request.META['QUERY_STRING']}")

            # validation
            if form.is_valid():
                print(form.cleaned_data)

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                price = form.cleaned_data.get("price")
                property_type = form.cleaned_data.get("property_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                bathrooms = form.cleaned_data.get("bathrooms")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # =========================================
                # QuerySets Filtering
                # 1. https://docs.djangoproject.com/en/2.2/ref/models/querysets/
                # 2. search "Field lookups"
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                # Even though property_types is a foreign key,
                # in case that we get the property_types from form.cleaned_data,
                # we don't have to use __pk
                if property_type is not None:  # if not Any kind
                    filter_args["property_type"] = property_type  # no __pk

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if bathrooms is not None:
                    filter_args["bathrooms__gte"] = bathrooms

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for a in amenities:
                    filter_args["amenities"] = a  # no __pk

                for f in facilities:
                    filter_args["facilities"] = f  # no __pk

                # print(f"Filtering Result: {filter_args}")

                qs_rooms = models.Room.objects.filter(**filter_args).order_by(
                    "name"
                )  # added order_by() to fix 'UnorderedObjectListWarning'

                paginator = Paginator(qs_rooms, 5, orphans=2)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                # return render(request, "rooms/search.html", {"form": form, "rooms": qs_rooms})
                return render(
                    # request, "rooms/search.html", {"form": form, "page": rooms, "query": request.META["QUERY_STRING"]}
                    request,
                    "rooms/search.html",
                    {"form": form, "page": rooms, "query": request.GET.urlencode},
                )
            else:
                print("form is invalid")

        else:  # if no country, then just pass an initial form without validation!
            print("we need a country for searching!")
            form = forms.SearchForm()  # Unbounded form

        # =========================================
        # Rendering
        return render(request, "rooms/search.html", {"form": form})


def search(request):
    """ search
        Function Based Room Search View
        """
    # =========================================
    # Search View in a manual way
    # =========================================
    """
    # =========================================
    # requests
    city = request.GET.get("city", "Anywhere")  # if no city key, set city = Anywhere
    city = str.capitalize(city or "Anywhere")  # if city is empty, set city = Anywhere
    country = request.GET.get("country", "")
    property_type = request.GET.get("property_type", 0)
    property_type = int(property_type or 0)
    price = int(request.GET.get("price", 0) or 0)
    guests = int(request.GET.get("guests", 0) or 0)
    bedrooms = int(request.GET.get("bedrooms", 0) or 0)
    beds = int(request.GET.get("beds", 0) or 0)
    bathrooms = int(request.GET.get("bathrooms", 0) or 0)
    instant_book = bool(request.GET.get("instant_book", False))  # on -> True by using bool()
    superhost = bool(request.GET.get("superhost", False))

    # requests with multi selection
    amenities = request.GET.getlist("amenities")
    facilities = request.GET.getlist("facilities")
    print(f"Selected Amenities: {amenities}")
    print(f"Selected Facilities: {facilities}")

    # =========================================
    # options
    property_types = models.PropertyType.objects.all()
    amenity_types = models.Amenity.objects.all()
    facility_types = models.Facility.objects.all()

    # =========================================
    # dictionaries for requests & options
    req = {
        "req_city": city,
        "req_country": country,
        "req_property_type": property_type,
        "req_price": price,
        "req_guests": guests,
        "req_bedrooms": bedrooms,
        "req_beds": beds,
        "req_bathrooms": bathrooms,
        "req_instant_book": instant_book,
        "req_superhost": superhost,
        "req_amenities": amenities,
        "req_facilities": facilities,
    }
    opt = {
        "opt_countries": countries,
        "opt_property_types": property_types,
        "opt_amenities": amenity_types,
        "opt_facilities": facility_types,
    }

    # =========================================
    # QuerySets Filtering
    # 1. https://docs.djangoproject.com/en/2.2/ref/models/querysets/
    # 2. search "Field lookups"
    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    # property_types is a foreign key, so we can filter it by pk
    if property_type != 0:  # if not Any kind
        filter_args["property_type__pk"] = property_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bathrooms != 0:
        filter_args["bathrooms__gte"] = bathrooms

    if instant_book is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    # filtering multi selections (many to many field)
    if len(amenities) > 0:
        for a in amenities:
            # amenities is a foreign key, so we can filter it by pk
            filter_args["amenities__pk"] = int(a)

    if len(facilities) > 0:
        for f in facilities:
            filter_args["facilities__pk"] = int(f)

    print(f"Filtering Result: {filter_args}")

    qs_rooms = models.Room.objects.filter(**filter_args)

    # =========================================
    # Rendering
    return render(
        request,
        "rooms/search.html",
        # set context by unpacking dictionary
        {**req, **opt, "rooms": qs_rooms},
    )
    """

    # =========================================
    # Search View with Django Forms
    # =========================================
    """
        Django Forms: https://docs.djangoproject.com/en/2.2/ref/forms/
    """
    qs_rooms = {}

    country = request.GET.get("country")
    if country:
        # How to pass request data into form:
        # Just By passing request.GET, we can store user requests!
        form = forms.SearchForm(request.GET)  # Bounded form

        # validation
        if form.is_valid():
            # if form is valid, print cleaned data
            print(f"search(): ${form.cleaned_data}")

            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            price = form.cleaned_data.get("price")
            property_type = form.cleaned_data.get("property_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            bathrooms = form.cleaned_data.get("bathrooms")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            # =========================================
            # QuerySets Filtering
            # 1. https://docs.djangoproject.com/en/2.2/ref/models/querysets/
            # 2. search "Field lookups"
            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            # Even though property_types is a foreign key,
            # in case that we get the property_types from form.cleaned_data,
            # we don't have to use __pk
            if property_type is not None:  # if not Any kind
                filter_args["property_type"] = property_type  # no __pk

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if bathrooms is not None:
                filter_args["bathrooms__gte"] = bathrooms

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            for a in amenities:
                filter_args["amenities"] = a  # no __pk

            for f in facilities:
                filter_args["facilities"] = f  # no __pk

            print(f"Filtering Result: {filter_args}")

            qs_rooms = models.Room.objects.filter(**filter_args)

    else:  # if no country, then just pass an initial form without validation!
        form = forms.SearchForm()  # Unbounded form

    # =========================================
    # Rendering
    return render(request, "rooms/search.html", {"form": form, "rooms": qs_rooms})
