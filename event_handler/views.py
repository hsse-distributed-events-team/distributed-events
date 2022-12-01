from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from event_handler.forms import EventForm
from event_handler.models import EventData

from db_controller import *


@login_required
def create_event(request):
    """
    Страница создания мероприятия

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    form = EventForm(request.POST)
    context = {'form': form}

    if form.is_valid():
        date = form.cleaned_data['date']
        name = form.cleaned_data['name']
        privacy = form.cleaned_data['privacy']

        user = request.user

        if user.is_authenticated:
            record = EventData(name=name,
                               date=date.strftime("%Y.%m.%d"),
                               privacy=privacy
                               )
            record.save()

    return render(request, 'create_event.html', context)


def all_events(request):
    context = {}
    return render(request, 'all_events/all_events.html', context)


def cur_event(request):
    context = {"event_id": request.GET.get("event_id")}
    event = get_event_by_id(context["event_id"])
    context['name'] = event.name
    context['description'] = event.description
    context['stages'] = [get_stages_by_event(context["event_id"])]
    return render(request, 'all_events/templates/cur_event.html', context)
