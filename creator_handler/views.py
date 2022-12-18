from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from creator_handler.db_controller import *
from .forms import StaffForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def add_staff(request):
    """
    Страница добавления участника

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """
    form = StaffForm()
    if request.method == "POST" and is_ajax(request):
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


# @login_required(login_url="login")
def view_participants(request, event_id):
    """
    Страница просмотра всех участников

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :param event_id: id мероприятия
    :type event_id: :class: 'int'
    :return: html страница
    """
    # if not user_have_access(request.user, event_id):
    #     return redirect('/404')
    context = {'participants_list': get_participants_by_event(get_event_by_id(event_id)),
               "navigation_buttons": [
                   {
                       'name': "Главная",
                       'href': "/"
                   },
                   {
                       'name': "Участники",
                       'href': "/participantes"
                   },
                   {
                       'name': "Площадки",
                       'href': "/venues"
                   },
                   {
                       'name': "Персонал",
                       'href': "/staff"
                   },
                   {
                       'name': "Настройки",
                       'href': "/settings"
                   }
               ]
    }

    return render(request, 'creator_handler/view_participants.html', context)

# @login_required(login_url="login")
def delete_participant(request, event_id: int):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == "POST" and is_ajax:
        print(request.POST)

        participant_id = request.POST.get('id', None)
        print(participant_id)
        if not user_have_access(request.user, event_id):
            return JsonResponse({"errors": "Not enough rights"}, status=400)
        # try:
        #     Venue.objects.get(id=participant_id).delete()
        #     return JsonResponse({}, status=200)
        # except ObjectDoesNotExist:
        #     print("А где")
        #     return JsonResponse({"errors": "There is no such venue"}, status=400)
        # except Exception as e:
        #     print(e)
        #     return JsonResponse({"errors": "Undefined server error"}, status=400)
    return JsonResponse({}, status=400)



@login_required
def view_staff(request):
    """
    Страница просмотра всех участников

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    context = {}

    return render(request, 'creator_handler/view_participants.html', context)
