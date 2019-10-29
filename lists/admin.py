from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.WishList)
class WishListAdmin(admin.ModelAdmin):

    """ WishList Admin Definition """

    list_display = ("name", "user", "count_rooms")

    search_fields = ("name",)

    filter_horizontal = ("rooms",)
