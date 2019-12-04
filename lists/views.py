from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from users import models as user_models
from . import models

# Create your views here.


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    # user = user_models.User.objects.get_or_none(email=request.user)
    user = request.user
    if room is not None and action is not None:
        # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#get-or-create
        wish_list, created = models.WishList.objects.get_or_create(
            user=request.user, name=f"{user.first_name}'s favourites"
        )
        # Edit Many-to-many relationships
        # https://docs.djangoproject.com/en/2.2/topics/db/examples/many_to_many/#many-to-many-relationships
        """ When you add or remove an item to ManyToManyField (room here), you don't need to call save().
            Just add() or remove() it """
        if action == "add":
            wish_list.rooms.add(room)
        elif action == "remove":
            wish_list.rooms.remove(room)

    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


""" def show_favs(request):
    user = request.user
    for fav_list in user.lists.all():
        print(fav_list.name)
    pass """


class ShowFavsView(TemplateView):

    template_name = "lists/detail.html"
