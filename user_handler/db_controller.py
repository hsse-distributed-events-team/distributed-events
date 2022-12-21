from .models import *


def create_user_for_django_user(django_user: DjangoUser) -> User:
    """
    Создание пользователя

    :param personal_data: информация о пользователе
    :return: user user
    """
    personal_data = PersonalData.objects.create()
    user = User.objects.create(user=django_user, personal_data=personal_data)
    return user


def add_region_of_user(username, region):
    """
    Добавление региона

    :param region: регион пользователя
    :return: user user

    """
    user = User.objects.get(user__username=username)
    user.personal_data.region = region
    user.personal_data.save()


def get_django_user(username):
    return DjangoUser.objects.get(username=username)


def get_user_by_id(user_id: int) -> User:
    return User.objects.get(id=user_id)
