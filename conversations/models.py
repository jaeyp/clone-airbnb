from django.db import models
from core.models import AbsctractTimeStampedModel

from users.models import User

# Create your models here.


class Conversation(AbsctractTimeStampedModel):

    """ Conversation Model Definition """

    name = models.CharField(default="", max_length=80)
    participants = models.ManyToManyField("users.User", related_name="conversations", blank=True)

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
            print(user.username)
        return f"{self.name} - {', '.join(usernames)}"  # str(self.created)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


class Message(AbsctractTimeStampedModel):

    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey("users.User", related_name="messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} says: {self.message}"
