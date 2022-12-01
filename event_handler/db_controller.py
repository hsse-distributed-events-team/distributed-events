from user_handler.models import User, PersonalData
from event_handler.models import Stage, Event

from django.contrib.auth.admin import User as DjangoUser
from django.db.models.query import QuerySet
from typing import Union, List, Tuple, Set

ITEMS_PER_PAGE = 10


def get_all_events(page=0, django_user: DjangoUser = None) -> Union[List, Union[Tuple, Event]]:
    event_ids = set()
    if django_user is not None:
        user = get_user_by_django_user(django_user)
        event_ids = get_user_events_id(user)
    result = list()
    if page == 0:
        events = Event.objects.all()
    else:
        events = Event.objects.all()[10 * (page - 1):10 * page]
    for event in events:
        if event.id in event_ids:
            result.append((event, True))
        else:
            result.append((event, False))
    return result


def get_user_events_id(user: User) -> Union[Set, int]:
    result = set()
    stages = get_user_stages(user)
    for stage in stages:
        result.add(stage.parent.id)
    return result


def get_user_stages(user: User) -> QuerySet:
    return user.stage_set.all()


def get_user_by_django_user(dj_user: DjangoUser) -> User:
    us = User.objects.get(user=dj_user)
    return us


def create_default_stage() -> Stage:
    stage = Stage()
    stage.save()
    return stage


def create_event(event: Event) -> None:
    Event.objects.create(event)


def get_event_by_id(id: int) -> Event:
    return Event.objects.get(id=id)


def get_stages_by_event(event: Event):
    return Stage.onjects.filter(parent=event)


def get_event_by_stage(stage: Stage) -> Event:
    return stage.parent
