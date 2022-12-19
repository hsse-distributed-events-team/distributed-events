from .models import *


def create_user_for_django_user(django_user: DjangoUser) -> User:
    """
    Создание объекта User с пустой PersonalData
    """

    personal_data = PersonalData.objects.create()
    user = User.objects.create(user=django_user, personal_data=personal_data)
    return user


def add_region_of_user(username, region):
    """
    Изменение региона пользователя с ником username
    """

    user = get_user(username)
    user.personal_data.region = region
    user.personal_data.save()


def get_django_user(username):
    """
    Получение обекта DjangoUser по полю username
    """

    return DjangoUser.objects.get(username=username)


def get_user(username):
    """
    Получение объекта User по полю username
    """

    user = User.objects.get(user__username=username)
    return user


def update_user_profile(data):
    """
    data - список передаваемых параметров.
    data[0] - username
    data[1] - email
    data[2] - name
    data[3] - surname
    data[4] - region
    Функция позволяет поменять данные о пользователе
    """

    user = get_user(username=str(data[0]))
    user.user.email = data[1]
    user.personal_data.name = data[2]
    user.personal_data.surname = data[3]
    user.personal_data.region = data[4]
    user.personal_data.save()
    user.user.save()
    # return user
