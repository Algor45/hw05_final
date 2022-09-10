"""Write your About app View functions here."""

from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Функция назначает template для страницы about/author."""

    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Функция назначает template для страницы about/tech."""

    template_name = 'about/tech.html'
