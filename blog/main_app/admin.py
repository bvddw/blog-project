from django.contrib import admin

# Register your models here.
from .models import Topic, Article, Comment

admin.site.register(Topic)
admin.site.register(Article)
admin.site.register(Comment)