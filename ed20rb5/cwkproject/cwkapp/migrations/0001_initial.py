# Generated by Django 4.1.7 on 2024-03-09 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='news',
            fields=[
                ('uniquekey', models.AutoField(primary_key=True, serialize=False)),
                ('headline', models.CharField(max_length=64)),
                ('catergory', models.CharField(choices=[('pol', 'Political'), ('art', 'Art'), ('tech', 'Technical'), ('trivia', 'Trivial')], max_length=6)),
                ('region', models.CharField(choices=[('uk', 'British News'), ('eu', 'European News'), ('w', 'World News')], max_length=2)),
                ('date', models.DateField()),
                ('details', models.CharField(max_length=128)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cwkapp.author')),
            ],
        ),
    ]
