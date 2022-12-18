from .models import *


def create_user_for_django_user(django_user: DjangoUser) -> User:
    personal_data = PersonalData.objects.create()
    user = User.objects.create(user=django_user, personal_data=personal_data)
    return user


def add_region_of_user(username, region):
    user = User.objects.get(user__username=username)
    user.personal_data.region = region
    user.personal_data.save()


def get_django_user(username):
    return DjangoUser.objects.get(username=username)
