"""Models for the hitcounter app."""

from django.db import models


class HitCounter(models.Model):
    """Model for hit counters."""

    page = models.CharField(max_length=255, editable=False)
    total = models.IntegerField(editable=False, default=0)
    trip = models.IntegerField(editable=False, default=0)

    def increment(self):
        """Increment hit counter."""
        self.total += 1
        self.trip += 1
        self.save()

    def reset_trip(self):
        """Reset trip to zero."""
        self.trip = 0
        self.save()
