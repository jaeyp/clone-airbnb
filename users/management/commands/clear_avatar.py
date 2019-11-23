from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command clear all avatars"

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            user.avatar.delete(save=True)
