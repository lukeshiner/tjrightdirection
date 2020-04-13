import factory
from pytest_factoryboy import register

from gallery import models


@register
class GalleryImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.GalleryImage

    image = factory.django.ImageField(width=800, height=200)
    thumbnail = factory.django.ImageField(width=200, height=50)
    width = 800
    height = 200
    thumb_width = 200
    thumb_height = 50
    order = 1
