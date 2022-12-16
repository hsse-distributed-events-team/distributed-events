from event_handler.models import Venue, StageStaff
from user_handler.models import DjangoUser, User

from event_handler.db_controller import get_user_by_django_user, get_stages_by_event, get_event_by_id


def get_venues_by_event(event_id: int):
    return Venue.objects.filter(parental_event_id=event_id)


def user_have_access(django_user: DjangoUser, event_id: int) -> bool:
    user = get_user_by_django_user(django_user)
    try:
        stage = get_stages_by_event(get_event_by_id(event_id)).first()
        print(user, stage)
        staff = StageStaff.objects.get(user=user, stage=stage)
        print(staff)
        return staff.status == StageStaff.Status.ACCEPTED
    except Exception as e:
        print(e)
        return False
