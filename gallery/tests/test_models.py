import pytest
from django.test import override_settings


@pytest.fixture(autouse=True)
def tmp_media_root(tmpdir):
    with override_settings(MEDIA_ROOT=tmpdir):
        yield


@pytest.mark.django_db
def test_str_method(gallery_image_factory):
    gallery_image = gallery_image_factory.create()
    assert str(gallery_image) == gallery_image.image.name


@pytest.mark.django_db
def test_filename_method(gallery_image_factory):
    image_name = "img.jpg"
    gallery_image = gallery_image_factory.create(image__filename=image_name)
    assert gallery_image.filename() == image_name


@pytest.mark.django_db
def test_thumb_filename_method(gallery_image_factory):
    image_name = "thumb.jpg"
    gallery_image = gallery_image_factory.create(image__filename=image_name)
    assert gallery_image.thumb_filename() == f"thumb_{image_name}"
