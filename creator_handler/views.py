from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .db_controller import *


@login_required
def venues_list(request, event_id: int):
    if not user_have_access(request.user, event_id):
        return redirect('/404')
    venues = get_venues_by_event(event_id)
    context = {
        "venues_list": venues,

    }
    return render(request, 'creator_handler/venues_list.html', context)

