from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . models import HitCounter


def hit_count(page_name):
    try:
        hit_counter = HitCounter.objects.get(page=page_name)
    except HitCounter.DoesNotExist:
        hit_counter = HitCounter(page=page_name)
    hit_counter.increment()


@login_required(login_url='admin:login')
def hit_counter(request):
    hit_counters = HitCounter.objects.all()
    return render(request, 'hitcounter/hitcounter.html', {
        'hit_counters': hit_counters})


def reset_trip(request, hit_counter_id):
    if not request.user.is_authenticated():
        return HttpResponseForbidden
    hit_counter = get_object_or_404(HitCounter, pk=hit_counter_id)
    hit_counter.reset_trip()
    return redirect('hitcounter:hit_counter')
