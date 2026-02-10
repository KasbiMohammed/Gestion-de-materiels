from django import template
from ..models import Visite

register = template.Library()

@register.simple_tag
def get_recent_visites(limit=5):
    """Retourne les visites les plus récentes"""
    return Visite.objects.select_related('materiel').order_by('-date_visite')[:limit]
