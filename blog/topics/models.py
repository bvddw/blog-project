from django.db import models
from main_app.models import UserModel


class Topic(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=255)
    users = models.ManyToManyField(UserModel, through='UserTopic')

    def __str__(self):
        return self.title


class UserTopic(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    notify = models.BooleanField(default=False)