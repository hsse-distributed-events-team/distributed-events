from .models import *


def create_user_for_django_user(django_user: DjangoUser) -> User:
    personal_data = PersonalData.objects.create()
    user = User.objects.create(user=django_user, personal_data=personal_data)
    return user


def add_region_of_user(username, region):
    user = get_user(username)
    user.personal_data.region = region
    user.personal_data.save()


def get_django_user(username):
    return DjangoUser.objects.get(username=username)


def get_user(username):
    user = User.objects.get(user__username=username)
    return user


def update_user_profile(data):
    user = get_user(username=str(data[0]))
    user.user.email = data[1]
    user.personal_data.name = data[2]
    user.personal_data.surname = data[3]
    user.personal_data.region = data[4]
    user.personal_data.save()
    user.user.save()
    # return user
