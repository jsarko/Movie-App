from django import template

register = template.Library()

@register.filter
def compare_genre(value, arg):
    genre_list = arg.genre.all()
    for g in genre_list:
        if value in g.name:
            return True
    return False