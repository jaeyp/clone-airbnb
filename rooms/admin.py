from django.contrib import admin

# mark_safe(): Explicitly mark a string as safe for (HTML) output purposes.
from django.utils.html import mark_safe

from . import models  # to access models.Room from models.py

# Register your models here.
@admin.register(models.PropertyType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    """ PhotoInline Admin Definition
        It allows RootAdmin page to have the admin menu of Photo
        since Photo refers to Room as its foreign key.
    """

    # InlineModelAdmin
    """
        Django provides two subclasses of InlineModelAdmin and they are:

        - TabularInline
        - StackedInline
        The difference between these two is merely the template used to render them.
    """

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):  # conneting admin pannel

    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        ("Basic info", {"fields": ("name", "description", "country", "city", "address", "price")}),
        ("Times", {"fields": ("check_in", "check_out", "instance_book")}),
        ("Spaces", {"fields": ("guest", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {"classes": ("collapse",), "fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guest",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instance_book",
        "count_amenities",  # function
        "count_photos",  # function
        "total_rating",
    )

    ordering = ("price", "guest", "beds", "bedrooms", "baths")

    list_filter = (
        "instance_book",
        "host__superhost",
        "property_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # InlineModelAdmin.raw_id_fields
    """
        By default, Django’s admin uses a select-box interface (<select>) for fields that are ForeignKey.
        raw_id_fields is a list of fields you would like to change into an Input widget for either a ForeignKey or ManyToManyField:
    """
    raw_id_fields = ("host",)

    # ModelAdmin.search_fields
    # Set search_fields to enable a search box on the admin change list page
    """
    Prefix	Lookup
    ^	    startswith
    =	    iexact
    @	    search
    None	icontains
    """
    search_fields = ("=city", "^host__username")

    # ModelAdmin.filter_horizontal
    # By adding a ManyToManyField to this list,
    # The unselected and selected options appear in two boxes side by side
    filter_horizontal = ("amenities", "facilities", "house_rules")

    # Overriding ModelAdmin.save_model()
    """
        When overriding ModelAdmin.save_model() and ModelAdmin.delete_model(), your code must save/delete the object. 
        They aren’t meant for veto purposes, rather they allow you to perform extra operations.
    """

    def save_model(self, request, obj, form, change):
        # do something before saving
        """ e.g.
            you can call send_mail() to admin user when admin data is changed from new ip address
        """

        super().save_model(request, obj, form, change)

        # do something else after saving

    def count_amenities(self, obj):
        # obj: __str__, obj.amenities.all(): QuerySet
        # print(f"[COMMON] {obj} {obj.amenities.all()}")
        return obj.amenities.count()

    # count_amenities.short_description = "you can change column name"

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # dir(): check a list of valid attributes for the file object
        # print(dir(obj.file))
        return mark_safe(f'<img src="{obj.file.url}" height="40px" />')

    get_thumbnail.short_description = "Thumbnail"
