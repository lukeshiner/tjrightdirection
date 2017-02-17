from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from . models import GalleryImage


class GalleryImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        'image', 'thumb_tag', 'width', 'height', 'thumb_width', 'thumb_height')

    def thumb_tag(self, obj):
        return obj.thumb_tag(height=75)

    thumb_tag.short_description = 'Thumbnail'
    thumb_tag.allow_tags = True


admin.site.register(GalleryImage, GalleryImageAdmin)
