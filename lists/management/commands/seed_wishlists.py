import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from rooms import models as room_models
from users import models as user_models


NAME = "wishlists"


class Command(BaseCommand):

    help = "This command generates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many {NAME} do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        """
            print(all_rooms)   # query_set (dict): list of key & value pair
            print(*all_rooms)  # list of value
        """
        seeder.add_entity(
            list_models.WishList, number, {"user": lambda x: random.choice(all_users)}
        )  # model, number, customFieldFormatters (dict or None)

        created_lists = seeder.execute()
        flatten_lists = flatten(created_lists.values())  # flatten list ([[]] => [])

        for pk in flatten_lists:
            wishlist = list_models.WishList.objects.get(pk=pk)
            # to_add = all_rooms[random.randint(0, 5) : random.randint(6, 20)]
            # wishlist.rooms.add(*to_add)
            for r in all_rooms:
                draw = random.randint(1, 10)
                if draw % 5 == 0:
                    wishlist.rooms.add(r)

            if len(wishlist.rooms.all()) == 0:
                wishlist.rooms.add(all_rooms[random.randint(0, len(all_rooms))])

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
