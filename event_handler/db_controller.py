from user_handler.models import User, PersonalData
from event_handler.models import Stage, Event, StageData, EventData


def get_all_events():
    pass


def get_user_stages():
    pass


def get_event_by_stage(stage: Stage) -> Event:
    return stage.parent


def get_stage_info(stage: Stage):
    pass
