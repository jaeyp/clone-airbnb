from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rooms.models import Room
from . import models

# Register your models here.

"""
# ModelAdmin objects - customizing Django’s admin interface
@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ("username", "email", "gender", "language", "currency", "superhost")
    list_filter = ("language", "currency", "superhost")
"""


class RoomInline(admin.TabularInline):  # admin.StackedInline

    """ RoomInline Admin Definition
        It allows UserAdmin page to have the admin menu of Room
        since Room refers to User as its foreign key.
    """

    model = Room


# UserAdmin objects - Customizing authentication in Django
@admin.register(models.User)  # decorator!
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    # If you are using a custom ModelAdmin which is a subclass of django.contrib.auth.admin.UserAdmin,
    # then you need to add your custom fields to fieldsets (for fields to be used in editing users)
    # and to add_fieldsets (for fields to be used when creating a user). For example:

    inlines = (RoomInline,)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )
    # adds custom filters to base filters
    list_filter = UserAdmin.list_filter + ("language", "currency", "superhost")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )


# this is the same with using decorator: @admin.register(models.User)
# admin.site.register(models.User, CustomUserAdmin)
