# core/custom_filters.py
import re
from django import template
from django.utils.text import slugify

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
    
@register.filter
def custom_slugify(value):
    slugified_value = slugify(value)
    if not slugified_value:
        slugified_value = re.sub(r'\W+', '-', value).strip('-').lower()
    print(f"Original: {value}, Slugified: {slugified_value}")
    return slugified_value