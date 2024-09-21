# core/custom_filters.py
from django import template

register = template.Library()

@register.filter
def ms_to_minutes_seconds(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"