from django.shortcuts import render
from . models import Recomendation


def recomendations(request):
    recomendations = Recomendation.objects.all()
    return render(request, 'recomendations/recomendations.html', {
        'recomendations': recomendations})
