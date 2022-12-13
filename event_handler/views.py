from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from event_handler.forms import Event as EventForm
from event_handler.models import Event as EventData

from event_handler.db_controller import *


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


def all_events(request, page_number=1):
    """
    Страница всех мероприятий

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    event_list = get_all_events(int(page_number), request.user)

    # if not event_list:
    #     return error404(request)

    context = {'event_list': event_list}

    return render(request, 'all_events.html', context)


def cur_event(request, event_id):
    """
    Страница конкретного мероприятия

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :param event_id: id мероприятия
    :type event_id: :class: 'int'
    :return: html страница
    """
    try:
        context = {"event_id": event_id}
        event = get_event_by_id(event_id)
        context['name'] = event.name
        context['description'] = event.description
        context['stages'] = [get_stages_by_event(context["event_id"])]
        return render(request, 'event.html', context)
    except ValueError:
        raise Http404
