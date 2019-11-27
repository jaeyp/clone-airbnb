from django.utils import timezone
from rooms import models as room_models
import calendar

# Custom Calendar Utility from Python Calendar
# https://docs.python.org/3/library/calendar.html


class Day:
    def __init__(self, number, is_past, booked=False):
        self.number = number
        self.is_past = is_past
        self.booked = booked

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month, room_pk):
        super().__init__(firstweekday=6)  # start from Sunday (6)
        self.year = year
        self.month = month
        self.room_pk = room_pk
        self.days_of_week = ("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_calendar_days_n_weeks(self):
        # get lists of seven tuples of day numbers and weekday numbers
        # https://docs.python.org/3/library/calendar.html#calendar.Calendar.monthdays2calendar
        days_n_weeks = self.monthdays2calendar(self.year, self.month)
        return days_n_weeks

    def get_calendar_days(self):
        days_n_weeks = self.monthdays2calendar(self.year, self.month)
        days = []

        # get room reservations
        room = room_models.Room.objects.get(pk=self.room_pk)
        reservations = room.get_reservations()  # .values_list("check_in", "check_out")
        print(reservations)
        for r in reservations:
            print(r.check_in.day, r.check_out.day)

        print(days_n_weeks)
        for week in days_n_weeks:
            # for day, weekday in week:  # unpacking tuple
            for day, _ in week:  # we don't care of 'weekday'
                now = timezone.now()
                is_past = (self.month == now.month and day <= now.day) or (
                    self.month < now.month and self.year <= now.year
                )

                # check if the day is already booked
                booked = False
                for r in reservations:
                    if self.month == r.check_in.month and day >= r.check_in.day and day < r.check_out.day:
                        booked = True

                new_day = Day(day, is_past, booked)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]


# cal = Calendar(2019, 11)
# print(cal.get_calendar_days_and_weeks())
# ~$ python ./util/cal.py
