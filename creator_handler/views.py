from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from .db_controller import *


@login_required(login_url="login")
def venues_list(request, event_id: int):

    if not user_have_access(request.user, event_id):
        return redirect('/404')
    venues = get_venues_by_event(event_id)
    context = {
        "venues_list": venues,
        "navigation_buttons" : [
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
    return render(request, 'creator_handler/venues_list.html', context)


@login_required(login_url="login")
def delete_venue(request, event_id: int):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == "POST" and is_ajax:
        print(request.POST)

        venue_id = request.POST.get('id', None)
        print(venue_id)
        if not user_have_access(request.user, event_id):
            return JsonResponse({"errors": "Not enough rights"}, status=400)
        try:
            Venue.objects.get(id=venue_id).delete()
            return JsonResponse({}, status=200)
        except ObjectDoesNotExist:
            print("А где")
            return JsonResponse({"errors": "There is no such venue"}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"errors": "Undefined server error"}, status=400)
    return JsonResponse({}, status=400)
