# Generated by Django 4.1.4 on 2022-12-14 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_alter_genre_id_alter_media_id_alter_providers_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='on_plex',
        ),
    ]
