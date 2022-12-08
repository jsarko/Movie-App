from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('lookup', views.lookup, name='lookup'),
    path('add', views.add, name='add'),
    path('add_to_plex', views.add_plex, name='add_plex')
]
