from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from creator_handler.db_controller import *
from .forms import StaffForm


@login_required
def add_staff(request):
    """
    Страница добавления участника

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """
    form = StaffForm()
    if request.method == "POST" and request.is_ajax():
        form = StaffForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['stage'].parent
            username = form.cleaned_data['username']
            form.save()
            return JsonResponse({'event_id': event_id,
                                 'username': username,
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

    context = {'participants_list': get_participants_by_event(get_event_by_id(event_id))}

    return render(request, 'creator_handler/view_participants.html', context)
