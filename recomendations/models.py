"""Models for the recomendations app."""

from django.db import models


class Recomendation(models.Model):
    """Model for recomendations."""

    text = models.TextField()
    name = models.CharField(null=True, blank=True, max_length=255)
    address = models.CharField(null=True, blank=True, max_length=255)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        """Sort objects."""

        ordering = ('order',)

    def __str__(self):
        return self.name
