# Generated by Django 2.0.2 on 2018-02-27 14:35

from django.db import migrations, models
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    for event in Event.objects.all():
        event.slug = slugify(str(event))
        event.save()


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_auto_20180223_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='', unique=False),
            preserve_default=False,
        ),
        migrations.RunPython(generate_slugs),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='', unique=True)
        )
    ]