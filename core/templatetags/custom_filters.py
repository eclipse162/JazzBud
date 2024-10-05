# core/custom_filters.py
from django import template

register = template.Library()

@register.filter
def ms_to_minutes_seconds(ms):
    try:
        ms = int(ms)
        total_seconds = ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    except (ValueError, TypeError):
        return "3:00"