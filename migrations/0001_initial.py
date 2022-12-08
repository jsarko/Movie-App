# Generated by Django 2.2.4 on 2019-12-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('rated', models.CharField(max_length=5)),
                ('released', models.DateField()),
                ('runtime', models.CharField(max_length=10)),
                ('director', models.CharField(max_length=255)),
                ('actors', models.CharField(max_length=255)),
                ('plot', models.TextField()),
                ('poster', models.URLField()),
                ('ratings', models.TextField()),
                ('media_type', models.CharField(max_length=30)),
                ('genre', models.ManyToManyField(to='movie_watch.Genre')),
            ],
        ),
    ]
