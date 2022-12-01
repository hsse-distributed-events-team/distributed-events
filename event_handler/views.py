from django.shortcuts import render

from event_handler.models import Event

# Create your views here.

def all_events(request):
    context = []
    if request.user.is_authenticated:
        pass
    return render(request, 'all_events.html', context)
