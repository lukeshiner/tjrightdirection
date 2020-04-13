import pytest
from django.shortcuts import reverse
from django.utils import timezone

from hitcounter.models import HitCounter


@pytest.fixture
def homepage_url():
    return "/"


@pytest.fixture()
def homepage_hitcounter(django_db_blocker):
    with django_db_blocker.unblock():
        hitcounter, _ = HitCounter.objects.get_or_create(page="Homepage")
    return hitcounter


@pytest.fixture
def homepage_response(homepage_hitcounter, client, homepage_url):
    return client.get(homepage_url)


@pytest.fixture
def homepage_content(homepage_response):
    return homepage_response.content.decode("utf8")


@pytest.mark.django_db
def test_homepage_status_code(homepage_response):
    assert homepage_response.status_code == 200


@pytest.mark.django_db
def test_homepage_uses_template(homepage_response):
    assert "tjhome/index.html" in (t.name for t in homepage_response.templates)


@pytest.mark.django_db
def test_homepage_increments_hitcounter(client, homepage_hitcounter, homepage_url):
    assert homepage_hitcounter.trip == 0
    assert homepage_hitcounter.total == 0
    client.get(homepage_url)
    homepage_hitcounter.refresh_from_db()
    assert homepage_hitcounter.trip == 1
    assert homepage_hitcounter.total == 1
    client.get(homepage_url)
    homepage_hitcounter.refresh_from_db()
    assert homepage_hitcounter.trip == 2
    assert homepage_hitcounter.total == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        reverse("tjhome:index"),
        reverse("gallery:gallery"),
        reverse("contact:contact"),
        reverse("recomendations:recomendations"),
    ],
)
def test_homepage_links(url, homepage_content):
    assert f'href="{url}"' in homepage_content


@pytest.mark.django_db
def test_homepage_footer(homepage_content):
    year = timezone.now().year
    assert f"&copy; Luke Shiner {year}" in homepage_content
