from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


NAME = "users"


class Command(BaseCommand):

    help = "This command generates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many {NAME} do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            User, number, {"is_staff": False, "is_superuser": False}
        )  # model, number, customFieldFormatters (dict or None)
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
