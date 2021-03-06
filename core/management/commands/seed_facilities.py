from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import Facility


class Command(BaseCommand):

    help = "This command generates facility options"

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):
        facilities = ["Free parking on premises", "Gym", "Hot tub", "Pool"]

        for f in facilities:
            Facility.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))


"""         def add_arguments(self, parser):
            parser.add_argument(
                "--times", help="How many times do you want me to tell you that I love you"
            ) """

"""         def handle(self, *args, **options):
            times = options.get("times")
            for t in range(0, int(times)):
                self.stdout.write(self.style.SUCCESS("I love you")) """
