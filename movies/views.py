from urllib import parse
import requests as r
import re, json
import ast

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.core import serializers

from .models import Media, Genre, Providers, Torrents

from movies.utilities.scrappers import Scrapper1337x
from movies.utilities.helpers import get1337xSearchUrl



def list_movies(request):
    media_filter = request.GET.get('filter', 'all')
    chosen_genre = request.GET.get('genre')
    if chosen_genre:
        # genre_obj = Genre.objects.get(name=chosen_genre)
        media = Media.objects.filter(genre_name=chosen_genre).all()
    else:
        media = Media.objects.all()

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
        print(f'Created New Entry: {created}')
        # Get providers
        print('Getting Providers...')
        providers = get_providers(title)
        for item in providers:
            print(f'Adding {item}')
            prov_obj, created = Providers.objects.get_or_create(name=item)
            media.providers.add(prov_obj)

        print('Updating genres...')
        for g in genre:
            print(f'Adding: {g}')
            genre_obj, created = Genre.objects.get_or_create(name=g)
            media.genre.add(genre_obj)
        params = f'?success={media_type} added successfully'
    except Exception as e:
        print(e)
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
    
    if auth_key == SECRET_KEY:
        media = Torrents.objects.filter(status="READY")
        data = serializers.serialize('json', media, fields=('pk', 'title'))
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