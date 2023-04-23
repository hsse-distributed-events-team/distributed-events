from user_handler.models import User, PersonalData
from event_handler.models import Stage, Event, StageStaff

from user_handler.db_controller import create_user_for_django_user

from django.contrib.auth.admin import User as DjangoUser
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from typing import Union, List, Tuple, Set

from itertools import chain

ITEMS_PER_PAGE = 12  # Количество объектов в одной странице выдачи


def get_all_events(django_user: DjangoUser = None) -> Union[List, Union[Tuple, Event, Stage, int]]:
    """
    Получить список всех мероприятий по заданным параметрам
    :param django_user: Пользователь, сделавший запрос
    :return: Список из троек: мероприятие, его первый этап, bool участвует ли django_user в этом мероприятии

    """

    user_events = set()
    if (not django_user.is_anonymous) and django_user is not None:
        user = get_user_by_django_user(django_user)
        user_events = get_user_events(user)

    result = list()
    events = Event.objects.all()
    for event in events:
        if event in user_events:
            result.append((event, event.stage_set.first, True))
        else:
            result.append((event, event.stage_set.first, False))
    return result


def get_user_events(user: User, user_role=0) -> Union[Set, int]:
    """
    :param user: Пользователь. Удивительно, да?
    :param user_role: Роль пользователя. (0 - все, 1 - участник, 2 - модератор)
    :return: Множество мероприятий, в которых участвует user
    """
    result = set()
    stages = get_user_stages(user, user_role)
    for stage in stages:
        result.add(stage.stage.parent)
    return result


def get_user_stages(user: User, user_role=0):
    """
    :param user: Пользователь. Удивительно, да?
    :param user_role: Роль пользователя. (0 - все, 1 - участник, 2 - модератор)
    :return: Список этапов, в которых участвует user
    """
    if user_role == 0:
        stages = list(chain(user.stageparticipants_set.all(), user.stagestaff_set.all()))
    elif user_role == 1:
        stages = list(user.stageparticipants_set.all())
    else:
        stages = list(user.stagestaff_set.all())
    return stages


def get_events_by_role(django_user: DjangoUser = None, user_role=0) -> Union[List, Union[Tuple, Event, Stage, int]]:
    """
    Получить список всех мероприятий по заданным параметрам
    :param django_user: Пользователь, сделавший запрос
    :param user_role: Роль пользователя. (0 - все, 1 - участник, 2 - модератор)
    :return: Список из троек: мероприятие, его первый этап, bool участвует ли django_user в этом мероприятии
    """

    user_events = set()
    if (not django_user.is_anonymous) and django_user is not None:
        user = get_user_by_django_user(django_user)
        user_events = get_user_events(user, user_role)

    result = list()
    for event in user_events:
        result.append((event, event.stage_set.first, True))
    return result


def get_user_by_django_user(django_user: DjangoUser) -> User:
    """

    :param dj_user: Пользователь в django-формате (обычно передаётся в качестве request.user)
    :return: User from user_handler

    """
    try:
        user = User.objects.get(user=django_user)
    except ObjectDoesNotExist:
        user = create_user_for_django_user(django_user=django_user)
    return user


def create_default_stage() -> Stage:
    stage = Stage()
    stage.save()
    return stage


def create_event(event: Event) -> None:
    Event.objects.create(event)


def get_event_by_id(id: int) -> Event:
    return Event.objects.get(id=id)


def get_stages_by_event(event: Event):
    return Stage.objects.filter(parent=event)


def get_open_stages_by_event(event: Event):
    waiting_status = Stage.Status.WAITING
    return list(filter(lambda stage: stage.settings.can_register,
                       Stage.objects.filter(parent=event, status=waiting_status)))


def get_event_by_stage(stage: Stage) -> Event:
    return stage.parent
