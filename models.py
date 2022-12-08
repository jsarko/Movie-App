from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Providers(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.URLField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Media(models.Model):
    imdbID = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=5)
    runtime = models.CharField(max_length=10)
    genre = models.ManyToManyField(Genre)
    director = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    plot = models.TextField()
    poster = models.URLField()
    rating = models.CharField(max_length=10)
    media_type = models.CharField(max_length=30)
    providers = models.ManyToManyField(Providers)
    on_plex = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.year}"

    class Meta:
        ordering = ['title']
