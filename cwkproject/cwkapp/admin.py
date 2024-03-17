from django.contrib import admin
from .models import Author, news

# Register your models here.
admin.site.register(Author)
admin.site.register(news)