"""Views for the tjhome app."""

from django.views.generic.base import TemplateView
from hitcounter.views import hit_count


class Index(TemplateView):
    """View for the homepage."""

    template_name = 'tjhome/index.html'

    def dispatch(self, *args, **kwargs):
        """Increment hit counter."""
        hit_count('Homepage')
        return super().dispatch(*args, **kwargs)
