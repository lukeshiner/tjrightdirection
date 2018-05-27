"""Model admin for the hitcounter app."""

from django.contrib import admin
from hitcounter import models


@admin.register(models.HitCounter)
class HitCounterAdmin(admin.ModelAdmin):
    """Model admin for the HitCounter model."""

    pass
