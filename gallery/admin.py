from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from . models import GalleryImage
from . forms import GalleryImageAdminForm


class GalleryImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = GalleryImageAdminForm
    list_display = (
        'image', 'thumb_tag', 'width', 'height', 'thumb_width', 'thumb_height')
    fieldsets = ((None, {'fields': ('images', )}), )

    def thumb_tag(self, obj):
        return obj.thumb_tag(height=75)

    thumb_tag.short_description = 'Thumbnail'
    thumb_tag.allow_tags = True

    def save_model(self, request, obj, form, change):
        for f in request.FILES.getlist('images'):
            new_image = GalleryImage(image=f)
            new_image.save()


admin.site.register(GalleryImage, GalleryImageAdmin)
