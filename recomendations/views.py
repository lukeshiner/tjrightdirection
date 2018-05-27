"""Views for the recomendations app."""

from django.views.generic.base import TemplateView

from .models import Recomendation


class Recomendations(TemplateView):
    """View for the recomendations page."""

    template_name = 'recomendations/recomendations.html'

    def get_context_data(self, *args, **kwargs):
        """Return context data for template."""
        context = super().get_context_data(*args, **kwargs)
        context['recomendations'] = Recomendation.objects.all()
        return context
