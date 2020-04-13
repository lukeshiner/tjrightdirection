import pytest
from django.shortcuts import reverse
from django.utils import timezone


@pytest.fixture
def recomendations(recomendation_factory):
    return [recomendation_factory.create() for _ in range(5)]


@pytest.fixture
def recomendations_url():
    return "/recomendations/"


@pytest.fixture
def recomendations_response(client, recomendations_url):
    return client.get(recomendations_url)


@pytest.fixture
def recomendations_content(recomendations_response):
    return recomendations_response.content.decode("utf8")


@pytest.mark.django_db
def test_recomendations_status_code(recomendations_response):
    assert recomendations_response.status_code == 200


@pytest.mark.django_db
def test_recomendations_uses_template(recomendations_response):
    assert "recomendations/recomendations.html" in (
        t.name for t in recomendations_response.templates
    )


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
def test_recomendations_links(url, recomendations_content):
    assert f'href="{url}"' in recomendations_content


@pytest.mark.django_db
def test_recomendations_footer(recomendations_content):
    year = timezone.now().year
    assert f"&copy; Luke Shiner {year}" in recomendations_content


@pytest.mark.django_db
def test_recomendations_are_displayed(recomendations, recomendations_content):
    for recomendation in recomendations:
        assert recomendation.text.replace("\n", "<br>") in recomendations_content
        assert recomendation.name in recomendations_content
        assert recomendation.address in recomendations_content
