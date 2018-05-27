"""Views for the gallery app."""

from django.views.generic.base import TemplateView
from gallery import models


class Gallery(TemplateView):
    """View for the image gallery."""

    template_name = 'gallery/gallery.html'

    def get_context_data(self, *args, **kwargs):
        """Return context for template."""
        context = super().get_context_data(*args, **kwargs)
        context['gallery_images'] = models.GalleryImage.objects.all()
        return context
