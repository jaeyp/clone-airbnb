from django.contrib import messages
from django.shortcuts import redirect, reverse
from rooms import models as room_models
from . import forms

# Create your views here.


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():  # call clean method
            review = form.save()  # get a review by using overriding save(commit=false)
            review.room = room
            review.user = request.user
            review.save()  # finally, put it on database
            messages.success(request, "Room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
