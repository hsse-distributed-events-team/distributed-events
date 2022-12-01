from user_handler.models import User, PersonalData
from event_handler.models import Stage, Event


def get_all_events():
    pass


def get_user_stages():
    pass


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
