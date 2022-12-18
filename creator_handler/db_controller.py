from event_handler.models import Event, Stage, StageStaff
from user_handler.models import DjangoUser, User

from event_handler.db_controller import get_user_by_django_user, get_stages_by_event, get_event_by_id


def get_participants_by_event(event: Event):
    stage = get_stages_by_event(event).first()
    return [] if stage.users is None else stage.users


def user_have_access(django_user: DjangoUser, event_id: int) -> bool:
    user = get_user_by_django_user(django_user)
    try:
        stage = get_stages_by_event(get_event_by_id(event_id)).first()
        # print(user, stage)
        staff = StageStaff.objects.get(user=user, stage=stage)
        # print(staff)
        return staff.status == StageStaff.Status.ACCEPTED
    except Exception as e:
        print(e)
        return False
