import pytest

from recomendations import models


@pytest.fixture
def test_text():
    return "Hello"


@pytest.fixture
def test_name():
    return "Joe"


@pytest.fixture
def test_address():
    return "12 Nostreet"


@pytest.mark.django_db
def test_recomendation_name_can_be_null(test_text, test_address):
    recomendation = models.Recomendation(
        text=test_text, name=None, address=test_address, order=1
    )
    recomendation.save()
    recomendation.refresh_from_db()
    assert recomendation.name is None


@pytest.mark.django_db
def test_recomendation_name_can_be_blank(test_text, test_address):
    recomendation = models.Recomendation(
        text=test_text, name="", address=test_address, order=1
    )
    recomendation.save()
    recomendation.refresh_from_db()
    assert recomendation.name == ""


@pytest.mark.django_db
def test_recomendation_address_can_be_null(test_text, test_name):
    recomendation = models.Recomendation(
        text=test_text, name=test_name, address=None, order=1
    )
    recomendation.save()
    recomendation.refresh_from_db()
    assert recomendation.address is None


@pytest.mark.django_db
def test_recomendation_address_can_be_blank(test_text, test_name):
    recomendation = models.Recomendation(
        text=test_text, name=test_name, address="", order=1
    )
    recomendation.save()
    recomendation.refresh_from_db()
    assert recomendation.address == ""


@pytest.mark.django_db
def test_recomendation_order_defaults_to_zero(test_text, test_name, test_address):
    recomendation = models.Recomendation(
        text=test_text, name=test_name, address=test_address
    )
    recomendation.save()
    recomendation.refresh_from_db()
    assert recomendation.order == 0


@pytest.mark.django_db
def test_recomendation_str_method(test_name, recomendation_factory):
    recomendation = recomendation_factory.create(name=test_name)
    assert str(recomendation) == test_name


@pytest.mark.django_db
def test_recomendation_ordering(recomendation_factory):
    for order in reversed(range(5)):
        recomendation_factory.create(order=order)
    recomendations = models.Recomendation.objects.all()
    for i, recomendation in enumerate(recomendations):
        assert recomendation.order == i
