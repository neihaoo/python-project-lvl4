"""Task Manager View Module."""

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index page view."""

    template_name = 'index.html'
