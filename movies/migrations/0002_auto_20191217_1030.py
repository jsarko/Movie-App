# Generated by Django 2.2.4 on 2019-12-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='ratings',
        ),
        migrations.AddField(
            model_name='media',
            name='rating',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]