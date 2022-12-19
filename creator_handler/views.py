from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import VenueForm
from .forms import EmailForm

import creator_handler.db_controller as c_db
import creator_handler.email as email

NAVIGATE_BUTTONS = [
    {
        'name': "Главная",
        'href': "/"
    },
    {
        'name': "Участники",
        'href': "../participantes"
    },
    {
        'name': "Площадки",
        'href': "../venues"
    },
    {
        'name': "Персонал",
        'href': "../staff"
    },
    {
        'name': "Настройки",
        'href': "../settings"
    }
]


@login_required(login_url="login")
def venues_list(request, event_id: int):
    if not c_db.user_have_access(request.user, event_id):
        return redirect('/404')
    venues = c_db.get_venues_by_event(event_id)
    context = {
        "venues_list": venues,
        "navigation_buttons": NAVIGATE_BUTTONS,
    }
    return render(request, 'creator_handler/venues_list.html', context)


@login_required(login_url="login")
def delete_venue(request, event_id: int):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == "POST" and is_ajax:
        venue_id = request.POST.get('id', None)
        if not c_db.user_have_access(request.user, event_id, c_db.SettingsSet.EDIT_VENUES):
            return JsonResponse({"errors": "Not enough rights"}, status=400)
        try:
            c_db.Venue.objects.get(id=venue_id).delete()
            return JsonResponse({}, status=200)
        except c_db.ObjectDoesNotExist:
            return JsonResponse({"errors": "There is no such venue"}, status=400)
        except Exception as e:
            print(e)  # - Заменить на логгирование
            return JsonResponse({"errors": "Undefined server error"}, status=400)
    return JsonResponse({}, status=400)


@login_required(login_url="login")
def create_venue(request, event_id: int):
    if not c_db.user_have_access(request.user, event_id, c_db.SettingsSet.EDIT_VENUES):
        return redirect("/404")
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            region = form.cleaned_data['region']
            participants_maximum = form.cleaned_data['participants_maximum']
            contacts = form.cleaned_data['contacts']
            c_db.create_venue(
                name,
                address,
                region,
                participants_maximum,
                contacts,
                event_id
            )
            return redirect(f'/events/edit/{event_id}/venues/')
    else:
        form = VenueForm()
    context = {
        "form": form,
    }
    return render(request, 'creator_handler/create_venue.html', context)


@login_required(login_url="login")
def edit_venue(request, event_id: int, venue_id: int):
    if not (c_db.user_have_access(request.user, event_id,
                                  c_db.SettingsSet.EDIT_VENUES) and c_db.is_venue_attached_to_event(event_id,
                                                                                                    venue_id)):
        return redirect("/404")
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            region = form.cleaned_data['region']
            participants_maximum = form.cleaned_data['participants_maximum']
            contacts = form.cleaned_data['contacts']
            c_db.edit_venue(name, address, region, participants_maximum, contacts, venue_id)
            return redirect(f'/events/edit/{event_id}/venues/')
    else:
        venue_data = c_db.get_venue_by_id_dict(venue_id)

        form = VenueForm(venue_data)
    context = {
        "form": form,
        "saved_form": venue_data,
    }
    return render(request, 'creator_handler/edit_venue.html', context)
def send_emal(request, event_id: int):
    if not c_db.user_have_access(request.user, event_id, c_db.SettingsSet.EDIT_VENUES):
        return redirect("/404")
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            email.send_message(..., text, subject)
            return redirect(f'/events/edit/{event_id}/participants/')
    else:
        form = EmailForm()
    context = {
        "form": form,
    }
    return render(request, 'creator_handler/send_email.html', context)
