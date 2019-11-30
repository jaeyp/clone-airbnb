import datetime
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from rooms import models as room_models
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
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


# why not DetailView here?
# because reservation detail view requires more manual access
class ReservationDetailView(View):
    """ Reservation Detail View Definition
    """

    # def get(self, pk):  # TypeError - get() got multiple values for argument 'pk'
    def get(self, request, pk):
        """ Move this code to CustomReservationManager
            try:
                reservation = models.Reservation.objects.get(pk=pk)
            except models.Reservation.DoesNotExist:
                pass
        """
        debug.info(pk)

        # and use .get_or_none() instead
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation:  # redirect to home if the reservation pk does not exist
            return redirect(reverse("core:home"))
        return render(self.request, "reservations/detail.html", {"reservation": reservation})
