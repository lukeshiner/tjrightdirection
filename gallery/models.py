"""Models for the gallery app."""

import os
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from PIL import Image


class GalleryImage(models.Model):
    """Model for gallery images."""

    image = models.ImageField(upload_to='gallery/images')
    thumbnail = models.ImageField(upload_to='gallery/thumbs', editable=False)
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)
    thumb_width = models.IntegerField(editable=False)
    thumb_height = models.IntegerField(editable=False)
    order = models.PositiveIntegerField(default=0)
    image_size = 800
    thumb_size = 200

    class Meta:
        """Sort gallery images."""

        ordering = ('order',)

    def __str__(self):
        return self.image.name

    def filename(self):
        """Return filename of the image."""
        return os.path.basename(self.image.name)

    def thumb_filename(self):
        """Return the filename of the thumbnail."""
        return os.path.basename(self.thumbnail.name)

    def image_tag(self, height='', width=''):
        """Return an HTML img tag for the image."""
        return '<img src="{}" height="{}" width="{}"/>'.format(
            self.image.url, height, width)

    def thumb_tag(self, height='', width=''):
        """Return an HTML img tag for the thumbnail."""
        return '<img src="{}" height="{}" width="{}"/>'.format(
            self.thumbnail.url, height, width)

    def save(self, *args, **kwargs):
        """Resize image and save object."""
        image = Image.open(self.image)
        self.width, self.height = image.size
        self.make_thumbnail(image)
        image = Image.open(self.image)
        self.make_fullsize_image(image)
        super(GalleryImage, self).save(*args, **kwargs)

    def get_thumb_size(self, image):
        """Return tuple of height and width for the thumbnail."""
        original_width, original_height = image.size
        if original_width > original_height:
            return (self.thumb_size, self.thumb_size)
        down_size_ratio = original_width / self.thumb_size
        adjusted_size = int(original_height / down_size_ratio)
        return (adjusted_size, adjusted_size)

    def get_full_size(self, image):
        """Return tuple of height and width for the image."""
        original_width, original_height = image.size
        if original_height <= self.image_size:
            return (original_width, original_height)
        down_size_ratio = original_height / self.image_size
        adjusted_width = int(original_width / down_size_ratio)
        adjusted_height = int(original_height / down_size_ratio)
        return (adjusted_width, adjusted_height)

    def save_image(
            self, image, original_filename, target_field,
            filename_template='{}{}'):
        """Resize and save image."""
        name, extension = os.path.splitext(original_filename)
        extension = extension.lower()
        filename = filename_template.format(name, extension)
        if extension in ('.jpg', '.jpeg'):
            file_type = 'JPEG'
        elif extension == '.png':
            file_type = 'PNG'
        else:
            raise Exception('File type not recognised: {}'.format(extension))
        temp_handle = BytesIO()
        image.save(temp_handle, file_type, optimize=True, quality=85)
        temp_handle.seek(0)
        uploaded_file = SimpleUploadedFile(
            name, temp_handle.read(),
            content_type='image/{}'.format(extension[1:]))
        target_field.save(filename, uploaded_file, save=False)
        temp_handle.close()

    def make_thumbnail(self, image):
        """Create thumbnail image."""
        image.thumbnail(
            self.get_thumb_size(image), Image.ANTIALIAS)
        self.thumb_width, self.thumb_height = image.size
        self.save_image(
            image, self.image.name, self.thumbnail,
            filename_template='thumb_{}{}')

    def make_fullsize_image(self, image):
        """Resize image."""
        resized_image = image.resize(
            self.get_full_size(image), Image.ANTIALIAS)
        self.width, self.height = resized_image.size
        self.save_image(resized_image, self.image.name, self.image)
