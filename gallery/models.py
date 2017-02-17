from io import StringIO, BytesIO
import os

from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/images')
    thumbnail = models.ImageField(upload_to='gallery/thumbs', editable=False)
    width = models.IntegerField(editable=False, blank=True, null=True)
    height = models.IntegerField(editable=False, blank=True, null=True)
    thumb_width = models.IntegerField(editable=False, blank=True, null=True)
    thumb_height = models.IntegerField(editable=False, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    thumb_size = 200

    def __str__(self):
        return self.image.name

    def filename(self):
        return os.path.basename(self.image.name)

    def thumb_filename(self):
        return os.path.basename(self.thumbnail.name)

    class Meta:
        ordering = ('order',)

    def save(self, *args, **kwargs):
        image = Image.open(self.image)
        self.width, self.height = image.size
        self.make_thumbnail(image)
        super(GalleryImage, self).save(*args, **kwargs)

    def get_thumb_size(self, image):
        original_width, original_height = image.size
        if original_width > original_height:
            return (self.thumb_size, self.thumb_size)
        down_size_ratio = original_width / self.thumb_size
        adjusted_thumb_size = int(original_height / down_size_ratio)
        return (adjusted_thumb_size, adjusted_thumb_size)

    def save_image(self, thumb_image):
        name, extension = os.path.splitext(self.image.name)
        extension = extension.lower()
        filename = 'thumb_{}{}'.format(name, extension)
        if extension in ('.jpg', '.jpeg'):
            file_type = 'JPEG'
        elif extension == '.gif':
            file_type = 'GIF'
        elif extension == '.png':
            file_type = 'PNG'
        else:
            raise Exception('File type not recognised: {}'.format(extension))
        temp_handle = BytesIO()
        thumb_image.save(temp_handle, file_type)
        temp_handle.seek(0)
        uploaded_file = SimpleUploadedFile(
            name, temp_handle.read(),
            content_type='image/{}'.format(extension[1:]))
        self.thumbnail.save(filename, uploaded_file, save=False)
        self.thumb_width, self.thumb_height = thumb_image.size
        temp_handle.close()

    def make_thumbnail(self, image):
        image.thumbnail(self.get_thumb_size(image), Image.ANTIALIAS)
        self.save_thumbnail(image)
