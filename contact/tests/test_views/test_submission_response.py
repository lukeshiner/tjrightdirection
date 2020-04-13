import pytest
from django.shortcuts import reverse
from django.utils import timezone


@pytest.fixture
def success_url():
    return "/contact/message_success/"


@pytest.fixture
def success_response(client, success_url):
    return client.get(success_url)


@pytest.fixture
def success_content(success_response):
    return success_response.content.decode("utf8")


def test_success_status_code(success_response):
    assert success_response.status_code == 200


def test_success_uses_template(success_response):
    assert "contact/success.html" in (t.name for t in success_response.templates)


@pytest.mark.parametrize(
    "url",
    [
        reverse("tjhome:index"),
        reverse("gallery:gallery"),
        reverse("contact:contact"),
        reverse("recomendations:recomendations"),
    ],
)
def test_success_links(url, success_content):
    assert f'href="{url}"' in success_content


def test_success_message(success_content):
    assert "Message sent successfully" in success_content


def test_success_footer(success_content):
    year = timezone.now().year
    assert f"&copy; Luke Shiner {year}" in success_content


@pytest.fixture
def failure_url():
    return "/contact/message_failure/"


@pytest.fixture
def failure_response(client, failure_url):
    return client.get(failure_url)


@pytest.fixture
def failure_content(failure_response):
    return failure_response.content.decode("utf8")


def test_failure_status_code(failure_response):
    assert failure_response.status_code == 200


def test_failure_uses_template(failure_response):
    assert "contact/failure.html" in (t.name for t in failure_response.templates)


@pytest.mark.parametrize(
    "url",
    [
        reverse("tjhome:index"),
        reverse("gallery:gallery"),
        reverse("contact:contact"),
        reverse("recomendations:recomendations"),
    ],
)
def test_failure_links(url, failure_content):
    assert f'href="{url}"' in failure_content


def test_failure_message(failure_content):
    assert "Message sending failed!" in failure_content


def test_failure_footer(failure_content):
    year = timezone.now().year
    assert f"&copy; Luke Shiner {year}" in failure_content
