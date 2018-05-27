"""Model admin for the gallery app."""

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from gallery import forms, models


@admin.register(models.GalleryImage)
class GalleryImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Model admin for the GalleryImage model."""

    form = forms.GalleryImageAdminForm
    list_display = (
        'image', 'thumb_tag', 'width', 'height', 'thumb_width', 'thumb_height')
    fieldsets = ((None, {'fields': ('images', )}), )

    def thumb_tag(self, obj):
        """Return thumb tag."""
        return obj.thumb_tag(height=75)

    thumb_tag.short_description = 'Thumbnail'
    thumb_tag.allow_tags = True

    def save_model(self, request, obj, form, change):
        """Save uploaded images."""
        for f in request.FILES.getlist('images'):
            new_image = models.GalleryImage(image=f)
            new_image.save()
