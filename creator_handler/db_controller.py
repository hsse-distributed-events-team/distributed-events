from event_handler.models import Event, Stage, StageStaff, StageParticipants, Venue
from creator_handler.models import StageSettings
from user_handler.models import DjangoUser, User

from django.core.exceptions import ObjectDoesNotExist
from enum import Enum

from event_handler.db_controller import get_user_by_django_user, get_stages_by_event, get_event_by_id


def get_participants_by_event(event: Event):
    stage = get_stages_by_event(event).first()
    return StageParticipants.objects.filter(stage=stage)


def get_staff_by_event(event: Event):
    stage = get_stages_by_event(event).first()
    return [] if stage.users is None else stage.users


class SettingsSet(Enum):
    EDIT_VENUES = 1
    ACCEPT_APPLICATIONS = 2
    MANAGE_MAILING_LIST = 3


def get_venues_by_event(event_id: int):
    return Venue.objects.filter(parental_event_id=event_id)


def get_venue_by_id(venue_id: int):
    return Venue.objects.get(id=venue_id)


def get_venue_by_id_dict(venue_id: int):
    try:
        venue = get_venue_by_id(venue_id)
    except ObjectDoesNotExist:
        venue = {}
    except Exception as e:
        print(e)
        venue = {}
    return venue


def user_have_access(django_user: DjangoUser, event_id: int, setting=-1) -> bool:
    user = get_user_by_django_user(django_user)
    try:
        stage = get_stages_by_event(get_event_by_id(event_id)).filter(next_stage__isnull=True).first()
        staff = StageStaff.objects.get(user=user, stage=stage)
        setting_rule = 0
        if setting == SettingsSet.EDIT_VENUES:
            setting_rule = stage.settings.who_can_edit_venues
        elif setting == SettingsSet.ACCEPT_APPLICATIONS:
            setting_rule = stage.settings.who_can_accept_applications
        elif setting == SettingsSet.MANAGE_MAILING_LIST:
            setting_rule = stage.settings.who_can_manage_mailing_list
        return staff.status == StageStaff.Status.ACCEPTED and staff.role >= setting_rule
    except ObjectDoesNotExist:
        return False


def create_venue(name: str, address: str, region: int, participants_maximum: int, contacts: str, event_id: int) -> None:
    try:
        Venue.objects.create(
            name=name,
            address=address,
            region=region,
            participants_maximum=participants_maximum,
            parental_event=get_event_by_id(event_id),
            contacts=contacts,
        )
    except Exception as e:
        print(e)


def edit_venue(name: str, address: str, region: int, participants_maximum: int, contacts: str, venue_id: int) -> None:
    try:
        venue = Venue.objects.filter(id=venue_id).update(
            name=name,
            address=address,
            region=region,
            participants_maximum=participants_maximum,
            contacts=contacts,
        )
    except Exception as e:
        print(e)


def is_venue_attached_to_event(event_id: int, venue_id: int) -> bool:
    try:
        venue = get_venue_by_id(venue_id)
        return venue.parental_event.id == event_id
    except ObjectDoesNotExist:
        return False


def register_on_event(event_id: int, venue_id: int, user: User):
    stage = get_stages_by_event(get_event_by_id(event_id)).first()
    venue = get_venue_by_id(venue_id)
    if not is_venue_attached_to_event(event_id, venue_id):
        raise ValueError

    participation = StageParticipants.objects.get_or_create(stage=stage, user=user)[0]
    participation.role = StageParticipants.Roles.PARTICIPANT
    participation.status = StageParticipants.Status.ACCEPTED
    participation.venue = venue
    participation.save()


def make_record_event(name, description):
    event = Event.objects.create(name=name, description=description)
    return event


def make_record_stage(name, event, preview="Пустое превью", time_start=None,
                      time_end=None, description="пустое описание", next_stage=None):
    stage = Stage.objects.create(
        name=name,
        parent=event,
        preview=preview,
        time_start=time_start,
        time_end=time_end,
        description=description,
        settings=StageSettings.objects.create(),
        next_stage=next_stage,
    )
    return stage


def get_stage_subtree(stage: int, to_delete):
    previous_stages = Stage.objects.filter(next_stage=stage).values_list('id', flat=True)
    for previous_stage in previous_stages:
        get_stage_subtree(previous_stage, to_delete)
    to_delete.append(stage)


def delete_stage_recursive(stage: int):
    to_delete = []
    get_stage_subtree(stage, to_delete)
    print(to_delete)
    Stage.objects.filter(id__in=to_delete).delete()


def create_staff(user, stage, role, status=Stage.Status.WAITING):
    StageStaff.objects.create(user=user,
                              stage=stage,
                              role=role,
                              status=status)


def reject_participant(user: User, event_id: int):
    try:
        stage = get_stages_by_event(get_event_by_id(event_id)).first()
        StageParticipants.objects.filter(user=user, stage=stage).update(status=StageParticipants.Status.REJECTED)
        return True
    except ObjectDoesNotExist:
        return False


def accept_participant(user: User, event_id: int):
    try:
        stage = get_stages_by_event(get_event_by_id(event_id)).first()
        StageParticipants.objects.filter(user=user, stage=stage).update(status=StageParticipants.Status.ACCEPTED)
        return True
    except ObjectDoesNotExist:
        return False


def ban_participant(user: User, event_id: int):
    try:
        stage = get_stages_by_event(get_event_by_id(event_id)).first()
        StageParticipants.objects.filter(user=user, stage=stage).update(status=StageParticipants.Status.BANNED)
        return True
    except ObjectDoesNotExist:
        return False


def get_event_partcipants(event_id: int):
    stage = get_stages_by_event(get_event_by_id(event_id)).first()
    return StageParticipants.objects.filter(stage=stage)


def get_formatted_stages(event_id: int):
    stages = get_stages_by_event(get_event_by_id(event_id))
    answer = []
    adjacency_list = {}
    final = -1
    fictive_stage = Stage(id=-1, name="fictive")
    stages_by_id = {-1: fictive_stage}
    for stage in stages:
        adjacency_list.setdefault(stage.id, []).append(fictive_stage.id)
    for stage in stages:
        stages_by_id[stage.id] = stage
        if stage.next_stage is not None:
            adjacency_list.setdefault(stage.next_stage.id, []).append(stage.id)
        else:
            final = stage.id
    if final == -1:
        raise ValueError
    for previous_stages in adjacency_list:
        adjacency_list[previous_stages].reverse()
    euler_bypass(final, adjacency_list, 0, answer, stages_by_id)
    return answer


def euler_bypass(stage: int, adjacency_list, depth: int, answer, stages_by_id):
    answer.append((stages_by_id[stage], depth))
    for previous_stage in adjacency_list.setdefault(stage, []):
        euler_bypass(previous_stage, adjacency_list, depth + 1, answer, stages_by_id)


def get_stage_by_id(stage_id: int):
    return Stage.objects.get(id=stage_id)
