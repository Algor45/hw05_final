"""Write your Core app tests here."""

from django.shortcuts import render


def page_not_found(request, exception):
    """Вызов View функции для кастомной страницы 404."""
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    """Вызов View функции для кастомной страницы 403csrf."""
    return render(request, 'core/403csrf.html')


def server_error(request):
    """Вызов View функции для кастомной страницы 500."""
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    """Вызов View функции для кастомной страницы 403."""
    return render(request, 'core/403.html', status=403)
