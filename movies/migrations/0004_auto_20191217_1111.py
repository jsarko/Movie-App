# Generated by Django 2.2.4 on 2019-12-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_media_imdbid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='released',
        ),
        migrations.AlterField(
            model_name='media',
            name='year',
            field=models.CharField(max_length=4),
        ),
    ]