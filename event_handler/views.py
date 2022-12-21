from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from event_handler.forms import Event as EventForm
from event_handler.forms import RegistrateEventForm

from event_handler.db_controller import *
from creator_handler.db_controller import *
import creator_handler.db_controller as c_db

from event_handler.models import Event, Stage, StageStaff

import event_handler.db_controller as e_db
import creator_handler.db_controller as c_db

NAVIGATE_BUTTONS = [
        {
            'name': "О нас",
            'href': "https://hsse.mipt.ru/"
        },
        {
            'name': "Создать мероприятие",
            'href': "/create_event"
        },
        {
            'name': "Профиль",
            'href': "/user_profile"
        }
    ]
]

def error404(request):
    """
    Страница 404 - page not found

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    return render(request, "404.html")


@login_required(login_url="login")
def create_event(request):
    """
    Страница создания мероприятия

    :param request: объект с деталями запроса
    :param context: информация о создаваемом мероприятии
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """
    context = {'page_name': "Создать мероприятие"}

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            # privacy = form.cleaned_data['privacy']
            preview = form.cleaned_data['preview']
            date_start = form.cleaned_data['date_start']
            print(date_start)
            date_finish = form.cleaned_data['date_finish']
            description = form.cleaned_data['description']

            user = c_db.get_user_by_django_user(request.user)

            event = c_db.make_record_event(name, description)
            stage = c_db.make_record_stage(name, event, preview, date_start, date_finish, description)
            c_db.create_staff(user, stage, StageStaff.Roles.PROVIDER, StageStaff.Status.ACCEPTED)

            return redirect('all_events')
        else:
            return HttpResponse('Invalid data')
    context['form'] = EventForm()
    return render(request, 'creator_handler/create_event.html', context)


def all_events(request):
    """
    Страница всех мероприятий

    :param request: объект с деталями запроса
    :param context: информация о всеx мероприятиях
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """
    event_list = get_all_events(request.user)

    context = {'page_name': 'Все мероприятия',
               'event_list': event_list,
               'navigation_buttons': [
                   {
                       'name': "О нас",
                       'href': "https://hsse.mipt.ru/"
                   },
                   {
                       'name': "Создать мероприятие",
                       'href': "/create_event"
                   },
                   {
                       'name': "Профиль",
                       'href': "../user_profile"
                   }
               ]
               }

    return render(request, 'event_handler/all_events.html', context)



@login_required(login_url="login")
def participant_event_list(request):
    """
    Страница всех мероприятий, в которых пользователь - участник

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    event_list = get_events_by_role(request.user, 1)

    # if not event_list:
    #     return error404(request)

    context = {'page_name': 'Мои мероприятия (Участник)',
               'event_list': event_list,
               'navigation_buttons': [
                   {
                       'name': "Главная",
                       'href': "/"
                   },
                   {
                       'name': "Профиль",
                       'href': "/user_profile"
                   }
               ]
               }

    return render(request, 'event_handler/all_events.html', context)


@login_required(login_url="login")
def staff_event_list(request):
    """
    Страница всех мероприятий, в которых пользователь - модератор

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    event_list = get_events_by_role(request.user, 2)

    # if not event_list:
    #     return error404(request)

    context = {'page_name': 'Мои мероприятия (Модератор)',
               'event_list': event_list,
               'navigation_buttons': [
                   {
                       'name': "Главная",
                       'href': "/"
                   },
                   {
                       'name': "Создать мероприятие",
                       'href': "/create_event/"
                   },
                   {
                       'name': "Профиль",
                       'href': "/user_profile"
                   }
               ]
               }

    return render(request, 'event_handler/all_events_for_staff.html', context)



def current_event(request, event_id):
    """
    Страница одного мероприятия

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :param event_id: id мероприятия
    :type event_id: :class: 'int'
    :return: html страница
    """
    try:
        event = e_db.get_event_by_id(event_id)
        context = {'page-name': f'{event.name}', 'navigation_buttons': [
            {
                'name': "Главная",
                'href': ".."
            },
            {
                'name': "Зарегистрироваться",
                'href': f"../event_registration/{event_id}"
            },
            {
                'name': "Профиль",
                'href': "../user_profile"
            }
        ]
                   }
        event = e_db.get_event_by_id(event_id)
        context['event_id'] = event_id
        context['name'] = event.name
        context['page_name'] = context['name']
        context['description'] = event.description
        context['stages'] = [e_db.get_stages_by_event(context["event_id"])]
        return render(request, 'event_handler/event.html', context)
    except ValueError:
        raise Http404


@login_required(login_url="login")
def current_event_registration(request, event_id):
    """
    Страница регистрации на мероприятие

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :param event_id: id мероприятия
    :type event_id: :class: 'int'
    :return: html страница
    """
    if request.method == "POST":
        form = RegistrateEventForm(request.POST)
        if form.is_valid():
            venue_id = form.cleaned_data['venue_id']
            user = get_user_by_django_user(request.user)
            c_db.register_on_event(event_id, venue_id, user)
            return redirect('all_events')

    context = {'navigation_buttons': [
        {
            'name': "Главная",
            'href': ".."
        },
        {
            'name': "Профиль",
            'href': "../user_profile"
        }
    ]
    }
    event = get_event_by_id(event_id)
    context['event_id'] = event_id
    context['name'] = event.name
    context['page-name'] = context['name']
    context['description'] = event.description
    context['venues_list'] = get_venues_by_event(event)
    context['stages'] = [get_stages_by_event(context["event_id"])]
    return render(request, 'event_handler/event_registration.html', context)

