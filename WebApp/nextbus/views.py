from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import BusForm
from .nextbus import NextBus

def index(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            bus_route = form.cleaned_data['bus_route']
            bus_stop = form.cleaned_data['bus_stop']
            direction = form.cleaned_data['direction']
            time_remaining = NextBus(bus_route, bus_stop, direction)
            return HttpResponse('<p>%s</p><p><a href="">Back</a></p>' % time_remaining)

    else:
        form = BusForm();

    return render(request, 'index.html',  {'form' : form})
