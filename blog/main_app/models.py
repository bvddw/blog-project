from django.utils import timezone
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

# Create your models here.
UserModel = get_user_model()


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


class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(validators=[MinLengthValidator(255)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topics = models.ManyToManyField(Topic)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title[:36]} {timezone.now().strftime('%Y-%d-%m')}")
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
