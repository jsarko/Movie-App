from urllib import parse
import requests as r
import re, json
import ast

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers

from .models import Media, Genre, Providers, Torrents

from movies.utilities.scrappers import Scrapper1337x
from movies.utilities.helpers import get1337xSearchUrl
from django.conf import settings



def list_movies(request):
    # TODO: Add cards/list view
    media_filter = request.GET.get('filter', 'all')
    chosen_genre = request.GET.get('genre')
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    media = Media.objects.filter(user=user.pk)
    if chosen_genre:
        # Because of how the genre logic is written media can have duplicated relationships in
        # the M2M table. Using distinct() corrects for this.
        media = media.filter(genre__name=chosen_genre).distinct()
    context = {
        'success': request.GET.get('success', ''),
        'error': request.GET.get('error', ''),
        'media': media,
        'genres': Genre.objects.all(),
        'filter': media_filter,
        'chosen_genre': chosen_genre
    }
    return render(request, 'movies/index.html', context)


def lookup(request):
    # http://www.omdbapi.com#usage
    # Escape all non safe chars.
    title = parse.quote(request.GET.get('title'))
    if re.search(r"^t{2}\d{6,}$", title):
        print("Searching By IMDb ID")
        url = f'http://www.omdbapi.com/?apikey=600f6be7&i={title}'
    else:
        url = f'http://www.omdbapi.com/?apikey=600f6be7&t={title}'
    response = r.get(url).json()
    context = {
        'data': response,
        'search': True
    }
    return render(request, 'movies/index.html', context)


def add(request):
    from .just_watch_api import get_providers
    params = ''
    if request.method == 'POST':
        dict_str = request.body.decode("UTF-8")
        data = ast.literal_eval(dict_str)
    else:
        data = request.GET

    title = data.get('title')
    year = data.get('year')
    runtime = data.get('runtime')
    genre = data.get('genre').split(', ')
    plot = data.get('plot')
    poster = data.get('poster')
    rated = data.get('rated')
    director = data.get('director')
    actors = data.get('actors')
    rating = data.get('rating')
    media_type = data.get('media_type')
    imdbID = data.get('imdbID')
    try:
        media, created = Media.objects.get_or_create(
            imdbID=imdbID,
            defaults={
                'title': title,
                'year': year,
                'runtime': runtime,
                'plot': plot,
                'poster': poster,
                'rated': rated,
                'director': director,
                'actors': actors,
                'rating': rating,
                'media_type': media_type,
                'imdbID': imdbID
            }
        )
        # Get providers
        providers = get_providers(title)
        for item in providers:
            print(f'Adding {item}')
            prov_obj, created = Providers.objects.get_or_create(name=item)
            media.providers.add(prov_obj)
        for g in genre:
            genre_obj, created = Genre.objects.get_or_create(name=g)
            media.genre.add(genre_obj)
        params = f'?success={media_type} added successfully'
    except Exception as e:
        params = f'?error={e}'

    return HttpResponse(status=204)


def add_plex(request):
    movie_id = request.GET.get('movie_id')
    media = Media.objects.filter(imdbID=movie_id)
    media.update(on_plex=True)
    data = {'success': f'Successfully added {movie_id} to plex.'}
    return JsonResponse(data, safe=False)

def list_to_download(request):
    auth_key = request.headers.get("AUTH_KEY")
    
    if auth_key == settings.API_SECRET_KEY:
        torrents = Torrents.objects.filter()
        data = serializers.serialize('json', torrents)
        return HttpResponse(data)
    return HttpResponse('Unauthorized', status=401)

def list_create_1337x_torrents(request):
    media_title = request.GET.get('title')
    search_url = get1337xSearchUrl(media_title)
    torrents = Scrapper1337x(url=search_url).list()
    # TODO: Use serializer
    return JsonResponse(
        torrents, 
        safe=False
    )

def create_torrent_download(request):
    if request.method == 'POST':
        dict_str = request.body.decode("UTF-8")
        data = ast.literal_eval(dict_str)
    else:
        return HttpResponseBadRequest()
    magnet = data.get('magnet')
    media_id = data.get('mediaId')
    print("Magnet:", magnet, "\nMediaId:", media_id)
    if not magnet or not media_id:
        return HttpResponseBadRequest()
    media = Media.objects.get(pk=media_id)
    torrent, wasCreated = Torrents.objects.get_or_create(media=media, defaults={"magnet": magnet, "status": "READY"})
    if wasCreated is False:
        torrent.magnet = magnet
        torrent.save()
        return HttpResponse(status=200)
    return HttpResponse(status=204)