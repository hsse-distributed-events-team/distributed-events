from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from creator_handler.db_controller import *
from .forms import ParticipantForm
import json


@login_required
def add_participant(request):
    """
    Страница добавления участника

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """
    form = ParticipantForm()
    if request.method == "POST" and request.is_ajax():
        form = ParticipantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            form.save()
            return JsonResponse({'name': name,
                                 'surname': surname,
                                 'email': email
                                 }, status=200)
        else:
            return JsonResponse({'errors': form.errors.as_json()}, status=400)

    return render(request, 'creator_handler/add_participant.html', {'form': form})


@login_required
def view_participants(request, event_id):
    """
    Страница просмотра всех участников

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :param event_id: id мероприятия
    :type event_id: :class: 'int'
    :return: html страница
    """

    context = {'participants_list': get_participants_by_event(event_id)}

    return render(request, 'creator_handler/view_participants.html', context)
