from django.shortcuts import render
from hitcounter.views import hit_count


def index(request):
    hit_count('Homepage')
    return render(request, 'tjhome/index.html')
