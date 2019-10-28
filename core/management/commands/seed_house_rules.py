from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import HouseRule


class Command(BaseCommand):

    help = "This command generates house rule options"

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):
        house_rules = ["Suitable for events", "Pets allowed", "Smoking allowed"]

        for r in house_rules:
            HouseRule.objects.create(name=r)

        self.stdout.write(self.style.SUCCESS(f"{len(house_rules)} house_rules created!"))


"""         def add_arguments(self, parser):
            parser.add_arguments(
                "--times", help="How many times do you want me to tell you that I love you"
            ) """

"""         def handle(self, *args, **options):
            times = options.get("times")
            for t in range(0, int(times)):
                self.stdout.write(self.style.SUCCESS("I love you")) """
