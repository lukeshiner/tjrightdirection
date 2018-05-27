"""Views for the hitcounter app."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse
from django.views.generic.base import RedirectView, TemplateView
from hitcounter import models


class UserLoginMixin(LoginRequiredMixin):
    """View mixin to enusure request comes from a logged in user."""

    login_url = 'admin:login'


def hit_count(page_name):
    """Increment hit counter."""
    try:
        hit_counter = models.HitCounter.objects.get(page=page_name)
    except models.HitCounter.DoesNotExist:
        hit_counter = HitCounter(page=page_name)
    hit_counter.increment()


class HitCounter(UserLoginMixin, TemplateView):
    """View hit counters."""

    template_name = 'hitcounter/hitcounter.html'

    def get_context_data(self, *args, **kwargs):
        """Return context for template."""
        context = super().get_context_data(*args, **kwargs)
        context['hit_counters'] = models.HitCounter.objects.all()
        return context


class ResetTrip(UserLoginMixin, RedirectView):
    """Reset trip and redirect to hit counter."""

    def get_redirect_url(self, *args, **kwargs):
        """Reset trip and redirect."""
        hit_counter = get_object_or_404(
            models.HitCounter, pk=self.kwargs['hit_counter_id'])
        hit_counter.reset_trip()
        return reverse('hitcounter:hit_counter')
