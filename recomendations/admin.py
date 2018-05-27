"""Model admin for the recomendations app."""

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from recomendations import models


@admin.register(models.Recomendation)
class RecomendationAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Model admin for the Recomendation model."""

    list_display = ('name', 'address')
