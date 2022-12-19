from django import template
import math
import re

register = template.Library()

@register.filter
def compare_genre(value, arg):
    genre_list = arg.genre.all()
    for g in genre_list:
        if value in g.name:
            return True
    return False

@register.filter
def toMinutesAndHours(value):
    # Use regex to extract numbers from string
    try:
        totalMinutes = int(value.replace(' min', ''))
        hours = math.floor(int(totalMinutes) / 60);
        minutes = totalMinutes % 60;
    except ValueError:
        hours, minutes = "N/A", "N/A"
    return f'{hours}:{minutes}';