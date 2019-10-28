import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command generates many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many rooms do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        property_types = room_models.PropertyType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.text()[: random.randint(10, 30)],
                "host": lambda x: random.choice(all_users),
                "property_type": lambda x: random.choice(property_types),
                "price": lambda x: random.randint(10, 500),
                "guests": lambda x: random.randint(1, 5),
                "beds": lambda x: random.randint(1, 8),
                "bedrooms": lambda x: random.randint(1, 5),
                "bathrooms": lambda x: random.randint(1, 3),
            },
        )  # model, number, customFieldFormatters (dict or None)
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
