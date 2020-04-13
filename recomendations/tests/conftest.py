import factory
from pytest_factoryboy import register

from recomendations import models

lorem = (
    "Lorem ipsum dolor sit amet, agam dictas te eos, te usu clita referrentur.\n"
    "No nam rationibus persequeris.\nEos imperdiet appellantur ea, vix cu "
    "officiis gubergren posidonium, copiosae vulputate adipiscing pri ut. In "
    "delicata voluptatibus ius, ea quot choro vel. Est ea putent possit "
    "urbanitas, timeam fuisset temporibus sit cu, vim ei movet aliquip."
)


@register
class RecomendationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Recomendation

    text = factory.Sequence(lambda n: f"{lorem} {n}")
    name = factory.Sequence(lambda n: f"Joe John {n}")
    address = factory.Sequence(lambda n: f"{n} Fake Street, Noto")
    order = 1
