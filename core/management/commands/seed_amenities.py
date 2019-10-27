from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command generates amenity options"

    def add_arguments(self, parser):
        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Washer",
            "Dryer",
            "Wifi",
            "Breakfast",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Laptop-friendly workspace",
            "TV",
            "Crib",
            "High chair",
            "Self check-in",
            "Smoke detector",
            "Carbon monoxide detector",
            "Private bathroom",
        ]

        for a in amenities:
            Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Amenities created!"))

    def handle(self, *args, **options):

        pass


"""         def add_arguments(self, parser):
            parser.add_arguments(
                "--times", help="How many times do you want me to tell you that I love you"
            ) """

"""         def handle(self, *args, **options):
            times = options.get("times")
            for t in range(0, int(times)):
                self.stdout.write(self.style.SUCCESS("I love you")) """
