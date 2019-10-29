import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
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
                "guests": lambda x: random.randint(1, 10),
                "beds": lambda x: random.randint(1, 8),
                "bedrooms": lambda x: random.randint(1, 5),
                "bathrooms": lambda x: random.randint(1, 3),
            },
        )  # model, number, customFieldFormatters (dict or None)

        created_rooms = seeder.execute()
        flatten_rooms = flatten(created_rooms.values())  # flatten list ([[]] => [])

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        print(created_rooms.values())
        for pk in flatten_rooms:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(5, random.randint(8, 20)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 57)}.webp",
                )
            for a in amenities:
                draw = random.randint(1, 10)
                if draw % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                draw = random.randint(1, 10)
                if draw % 2 == 0:
                    room.facilities.add(f)
            for r in house_rules:
                draw = random.randint(1, 10)
                if draw % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
