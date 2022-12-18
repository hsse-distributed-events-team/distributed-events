from .models import *


def create_user_for_django_user(django_user: DjangoUser) -> User:
    personal_data = PersonalData.objects.create()
    user = User.objects.create(user=django_user, personal_data=personal_data)
    return user
