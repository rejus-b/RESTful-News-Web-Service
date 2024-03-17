# Generated by Django 4.1.7 on 2024-03-14 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cwkapp', '0004_author_password_author_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='author',
        ),
        migrations.RemoveField(
            model_name='author',
            name='password',
        ),
        migrations.RemoveField(
            model_name='author',
            name='username',
        ),
        migrations.AddField(
            model_name='author',
            name='authorName',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]
