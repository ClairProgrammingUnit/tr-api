from django import forms

class BusForm(forms.Form):
    bus_route = forms.CharField(label = 'Bus Route')
    bus_stop = forms.CharField(label = 'Bus Stop')
    direction = forms.CharField(label = 'Direction')
