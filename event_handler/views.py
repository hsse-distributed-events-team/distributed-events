from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from event_handler.forms import Event
from event_handler.models import Event, Stage

from db_controller import *


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


def cur_event(request):
    context = {"event_id": request.GET.get("event_id")}
    event = get_event_by_id(context["event_id"])
    context['name'] = event.name
    context['description'] = event.description
    context['sub_events'] = [get_stages_by_event(context["event_id"])]
    return render(request, 'all_events/templates/cur_event.html', context)


def all_events(request):
    context = []
    if request.user.is_authenticated:
        pass
    return render(request, 'all_events.html', context)
