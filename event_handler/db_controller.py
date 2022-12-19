from user_handler.models import User, PersonalData
from event_handler.models import Stage, Event, StageStaff

from user_handler.db_controller import create_user_for_django_user

from django.contrib.auth.admin import User as DjangoUser
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from typing import Union, List, Tuple, Set

ITEMS_PER_PAGE = 12  # Количество объектов в одной странице выдачи


def get_all_events(page=0, django_user: DjangoUser = None) -> Union[List, Union[Tuple, Event, Stage, int]]:
    """
    Получить список всех мероприятий по заданным параметрам
    :param page: Номер страницы отображения
    :param django_user: Пользователь, сделавший запрос
    :return: Список из троек: мероприятие, его первый этап, bool участвует ли django_user в этом мероприятии
    """
    event_ids = set()
    if (not django_user.is_anonymous) and django_user is not None:
        user = get_user_by_django_user(django_user)
        event_ids = get_user_events_id(user)
    result = list()
    if page == 0:
        events = Event.objects.all()
    else:
        events = Event.objects.all()[10 * (page - 1):10 * page]
    for event in events:
        if event.id in event_ids:
            result.append((event, event.stage_set.first, True))
        else:
            result.append((event, event.stage_set.first, False))
    return result


def get_user_events_id(user: User) -> Union[Set, int]:
    """
    :param user: Пользователь. Удивительно, да?
    :return: Множество id мероприятий, в которых участвует user
    """
    result = set()
    stages = get_user_stages(user)
    for stage in stages:
        result.add(stage.parent.id)
    return result


def get_user_stages(user: User) -> QuerySet:
    return user.stageparticipants_set.all()


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


def get_event_by_stage(stage: Stage) -> Event:
    return stage.parent



