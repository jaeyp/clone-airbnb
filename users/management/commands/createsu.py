from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User


NAME = "users"


class Command(BaseCommand):

    help = "This command creates a Django superuser on AWS EB"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=settings.SU_USERNAME)
        if not admin:
            User.objects.create_superuser(settings.SU_USERNAME, settings.SU_EMAIL, settings.SU_PASSWORD)
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
