from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from . models import GalleryImage


class GalleryImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('image', 'width', 'height', 'thumb_width', 'thumb_height')


admin.site.register(GalleryImage, GalleryImageAdmin)
