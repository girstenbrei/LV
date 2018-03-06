# Generated by Django 2.0.2 on 2018-03-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forename', models.CharField(max_length=126)),
                ('lastname', models.CharField(max_length=126)),
                ('born', models.DateField()),
                ('plz', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=254)),
                ('group', models.CharField(max_length=254)),
                ('mail', models.EmailField(max_length=254)),
                ('perks', models.CharField(blank=True, max_length=254)),
                ('additional', models.TextField(blank=True)),
                ('next_station', models.CharField(max_length=254)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
