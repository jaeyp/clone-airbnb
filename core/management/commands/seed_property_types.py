from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import PropertyType


class Command(BaseCommand):

    help = "This command generates property type options"

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):
        property_types = [
            "House",
            "Apartment",
            "Bed and breakfast",
            "Boutique hotel",
            "Bungalow",
            "Cabin",
            "Chalet",
            "Cottage",
            "Guest suite",
            "Guesthouse",
            "Hostel",
            "Hotel",
            "Loft",
            "Resort",
            "Townhouse",
            "Villa",
        ]

        for t in property_types:
            PropertyType.objects.create(name=t)

        self.stdout.write(self.style.SUCCESS(f"{len(property_types)} property_types created!"))


"""         def add_arguments(self, parser):
            parser.add_argument(
                "--times", help="How many times do you want me to tell you that I love you"
            ) """

"""         def handle(self, *args, **options):
            times = options.get("times")
            for t in range(0, int(times)):
                self.stdout.write(self.style.SUCCESS("I love you")) """
