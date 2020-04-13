from unittest.mock import Mock, patch

import pytest
from django.conf import settings
from django.core import mail
from django.shortcuts import reverse
from django.utils import timezone

from contact import forms


@pytest.fixture
def url():
    return "/contact/"


@pytest.fixture
def form_data():
    return {
        "return_email": "jo@nowhere.com",
        "contact_name": "Joe John",
        "message_subject": "Information Request",
        "contact_phone": "0688547",
        "message_content": "The contents of the message.",
    }


@pytest.fixture
def get_response(client, url):
    return client.get(url)


@pytest.fixture
def post_response(client, url, form_data):
    return client.post(url, form_data)


@pytest.fixture
def get_content(get_response):
    return get_response.content.decode("utf8")


@pytest.fixture
def sent_email(post_response):
    return mail.outbox[0]


@pytest.fixture
def email_error_contact_form():
    with patch("contact.views.ContactForm") as mock_ContactForm:
        mock_contact_form = Mock()
        mock_contact_form.is_valid.return_value = True
        mock_contact_form.send_mail.side_effect = Exception()
        mock_ContactForm.return_value = mock_contact_form
        yield mock_contact_form


def test_get_status_code(get_response):
    assert get_response.status_code == 200


def test_uses_template(get_response):
    assert "contact/contact.html" in (t.name for t in get_response.templates)


@pytest.mark.parametrize(
    "link",
    [
        reverse("tjhome:index"),
        reverse("gallery:gallery"),
        reverse("contact:contact"),
        reverse("recomendations:recomendations"),
    ],
)
def test_links(link, get_content):
    assert f'href="{link}"' in get_content


def test_footer(get_content):
    year = timezone.now().year
    assert f"&copy; Luke Shiner {year}" in get_content


def test_post_status_code(post_response):
    assert post_response.status_code == 302


def test_successful_post_redirect(post_response):
    assert post_response.url == reverse("contact:success")


def test_form_does_not_email(client, url, form_data):
    del form_data["return_email"]
    response = client.post(url, form_data)
    assert response.url == reverse("contact:success")
    assert len(mail.outbox) == 1


def test_form_requires_name(client, url, form_data):
    del form_data["contact_name"]
    response = client.post(url, form_data)
    assert forms.NO_NAME_MESSAGE in response.content.decode("utf8")
    assert len(mail.outbox) == 0


def test_form_requires_subject(client, url, form_data):
    del form_data["message_subject"]
    response = client.post(url, form_data)
    assert forms.NO_SUBJECT_MESSAGE in response.content.decode("utf8")
    assert len(mail.outbox) == 0


def test_form_does_not_require_contact_phone(client, url, form_data):
    del form_data["contact_phone"]
    response = client.post(url, form_data)
    assert response.url == reverse("contact:success")
    assert len(mail.outbox) == 1


def test_form_requires_message(client, url, form_data):
    del form_data["message_content"]
    response = client.post(url, form_data)
    assert forms.NO_CONTENT_MESSAGE in response.content.decode("utf8")
    assert len(mail.outbox) == 0


def test_invalid_email_address_is_not_allowed(client, url, form_data):
    form_data["return_email"] = "invalid_address"
    response = client.post(url, form_data)
    assert forms.INVALID_EMAIL_ADDRESS_MESSAGE in response.content.decode("utf8")
    assert len(mail.outbox) == 0


def test_form_sends_email(post_response):
    assert len(mail.outbox) == 1


def test_email_subject(form_data, sent_email):
    subject = form_data["message_subject"]
    name = form_data["contact_name"]
    assert sent_email.subject == f"Contact Form message from {name} Re: {subject}"


def test_email_body(form_data, sent_email):
    for key in ("contact_name", "return_email", "contact_phone", "message_content"):
        assert form_data[key] in sent_email.body


def test_email_from_address(sent_email):
    assert sent_email.from_email == settings.EMAIL_HOST_USER


def test_email_to_address(sent_email):
    assert sent_email.to == [settings.CONTACT_FORM_TARGET_ADDRESS]


def test_email_error(email_error_contact_form, client, form_data, url):
    response = client.post(url, form_data)
    assert response.url == reverse("contact:failure")
