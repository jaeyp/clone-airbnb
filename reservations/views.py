import datetime
from django.http import Http404
from django.views.generic import View, DetailView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from rooms import models as room_models
from reviews import forms as review_forms
from . import models
from util import debug

# Create your views here.


class CreateError(Exception):
    pass


def create(request, room_pk, year, month, day, days):
    debug.info(f"{room_pk} {year} {month} {day} {days}")
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room_pk)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user, room=room, check_in=date_obj, check_out=date_obj + datetime.timedelta(days=days),
        )
        debug.info(reservation.pk)
        # return redirect(reverse("core:home"))
        # return redirect(reverse("reservations:review", kwargs={"pk": reservation.pk}))
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationReviewView(DetailView):
    """ Reservation Review View Definition
    """

    model = models.Reservation
    template_name = "reservations/review.html"


# why not DetailView here?
# because reservation detail view requires more manual access
class ReservationDetailView(View):
    """ Reservation Detail View Definition
    """

    """ TypeError - get() got multiple values for argument 'pk'
        # wrong way
        def get(self, pk):

        # right way
        def get(self, request, pk):
            or
        def get(self, *args, **kwargs):
            pk = kwargs.get("pk")
    """

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        """ Overriding get() by using a custom manager (CustomModelManager)
            in order to filter a request accessing a reservation which doen't exist
        """
        debug.info(pk)

        # Move this code to CustomModelManager
        """
            try:
                reservation = models.Reservation.objects.get(pk=pk)
            except models.Reservation.DoesNotExist:
                pass
        """
        # and use .get_or_none() instead
        reservation = models.Reservation.objects.get_or_none(pk=pk)

        # raise Http404
        # if the reservation pk does not exist
        # or user is neither a guest nor a host
        if not reservation or (
            reservation.guest != self.request.user  # not a guest
            and reservation.room.home != self.request.user  # not a host
        ):
            raise Http404()

        # set reviews/form for reservations/template (detail.html)
        form = review_forms.CreateReviewForm()
        return render(self.request, "reservations/detail.html", {"reservation": reservation, "form": form})


def edit(request, pk, command):
    reservation = models.Reservation.objects.get_or_none(pk=pk)

    # raise Http404
    # if the reservation pk does not exist
    # or user is neither a guest nor a host
    if not reservation or (reservation.guest != request.user and reservation.room.home != request.user):
        raise Http404()

    if command == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif command == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        # if reservation is canceled, delete all the booked days related to the reservation
        models.BookedDay.objects.filter(reservation=reservation).delete()

    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
