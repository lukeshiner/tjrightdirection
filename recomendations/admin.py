from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from . models import Recomendation


class RecomendationAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'address')


admin.site.register(Recomendation, RecomendationAdmin)
