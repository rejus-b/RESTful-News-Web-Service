from django.db import models
from django.contrib.auth.models import User


catergory_choices = [('pol', "Political"), ('art', "Art"), ('tech', "Technical"), ('trivia', "Trivial")]
region_choices = [('uk', "British News"), ('eu', "European News"), ('w', "World News")]

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    authorName = models.CharField(max_length=128)
    # author = models.CharField(max_length=128)
    # username = models.CharField(max_length=64, unique=True)
    # password = models.CharField(max_length=128)

class news(models.Model):
    uniquekey = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    catergory = models.CharField(max_length=6, choices=catergory_choices)
    region = models.CharField(max_length=2, choices=region_choices)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    date = models.DateField()
    details = models.CharField(max_length=128)