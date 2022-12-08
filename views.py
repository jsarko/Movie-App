from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Media, Genre, Providers
import json
# Create your views here.


def index(request):
    media_filter = request.GET.get('filter', 'all')
    chosen_genre = request.GET.get('genre')
    if chosen_genre:
        genre_obj = Genre.objects.get(name=chosen_genre)
        media = Media.objects.filter(genre=genre_obj).all()
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
    return render(request, 'movie_watch/index.html', context)


def lookup(request):
    from urllib import parse
    import requests as r
    import json
    import re
    # http://www.omdbapi.com#usage
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
    return render(request, 'movie_watch/index.html', context)


def add(request):
    from .just_watch_api import get_providers
    params = ''

    title = request.GET.get('title')
    year = request.GET.get('year')
    runtime = request.GET.get('runtime')
    genre = request.GET.get('genre').split(', ')
    plot = request.GET.get('plot')
    poster = request.GET.get('poster')
    rated = request.GET.get('rated')
    director = request.GET.get('director')
    actors = request.GET.get('actors')
    rating = request.GET.get('rating')
    media_type = request.GET.get('media_type')
    imdbID = request.GET.get('imdbID')
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

    return HttpResponseRedirect(f'/movies{params}')


def add_plex(request):
    movie_id = request.GET.get('movie_id')
    media = Media.objects.filter(imdbID=movie_id)
    media.update(on_plex=True)
    data = {'success': f'Successfully added {movie_id} to plex.'}
    return JsonResponse(data, safe=False)
