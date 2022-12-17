from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .db_controller import *


@login_required(login_url="login")
def venues_list(request, event_id: int):
    if not user_have_access(request.user, event_id):
        return redirect('/404')
    venues = get_venues_by_event(event_id)
    context = {
        "venues_list": venues,

    }
    return render(request, 'creator_handler/venues_list.html', context)


@login_required(login_url="login")
def delete_venue(request, event_id: int, venue_id):
    if request.method == "POST" and request.is_ajax():
        if not user_have_access(request.user, event_id):
            return JsonResponse({"reason": "Not enough rights"}, status=400)
        try:
            Venue.objects.get(id=venue_id).delete()
            return JsonResponse({"reason": None}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"reason": "There is no such venue"}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"reason": "Undefined server error"}, status=400)
    return redirect('/')
