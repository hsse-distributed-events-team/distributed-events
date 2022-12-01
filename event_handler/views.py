from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from event_handler.forms import Event
from event_handler.models import Event
from django.views.generic import DetailView


@login_required
def create_event(request):
    """
    Страница создания мероприятия

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    form = Event(request.POST)
    context = {'form': form}

    with open("static/txt/create_event.txt") as f:
        context['info'] += f.readline()

    if form.is_valid():
        date = form.cleaned_data['date']
        name = form.cleaned_data['name']
        privacy = form.cleaned_data['privacy']

        user = request.user

        if user.is_authenticated:
            record = Event()
            record.save()

    return render(request, 'create_event.html', context)


def all_events(request):
    context = []
    return render(request, 'all_events/all_events.html', context)

class EventDetailView(DetailView):
    model = ""

def cur_event(request):
    context = {}
    context['name'] = Event.name
    context['date'] = Event.date
    context['info'] = "default"
    context['sub_events'] = {}
    return render(request, 'all_events/templates/cur_event.html', context)