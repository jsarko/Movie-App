from django.contrib import admin
from .models import Media, Genre, Providers
# Register your models here.

admin.site.register([Media, Genre, Providers])