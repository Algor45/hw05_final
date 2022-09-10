"""Write your template tags here."""

from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Set Custom filter addclass."""
    return field.as_widget(attrs={'class': css})
