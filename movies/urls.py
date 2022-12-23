from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.list_movies, name='list_movies'),
    path('lookup', views.lookup, name='lookup'),
    path('add', views.add, name='add'),
    path('add_to_plex', views.add_plex, name='add_plex'),
    path('download', views.list_to_download, name="list_to_download"),
    path('download/add', views.create_torrent_download, name="create_torrent_download"),
    path('torrents/1337x', views.list_create_1337x_torrents, name="list_1337x"),
]
