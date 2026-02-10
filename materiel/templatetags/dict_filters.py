from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Permet d'accéder à une valeur dans un dictionnaire avec une clé
    """
    return dictionary.get(key, None)
