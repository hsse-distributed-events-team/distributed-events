from django.db import models
from django.contrib.auth.models import User as DjangoUser


class PersonalData(models.Model):
    name = models.CharField('Имя', max_length=20)
    surname = models.CharField('Фамилия', max_length=20)
    # Пока что в стадии заглушки. Возможно расширить без ущерба для производства


class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name="django_user")
    personal_data = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField('Проверенный пользователь', default=False)


class EventData(models.Model):
    data = models.TextField(null=True, blank=True, max_length=500)
    # Пока что в ставдии заглушки.


class Event(models.Model):
    name = models.CharField("Название мероприятия", default="Новое мероприятие", max_length=50)
    data = models.OneToOneField(EventData, on_delete=models.CASCADE)


class StageData(models.Model):
    data = models.TextField(null=True, blank=True, max_length=500)
    # Пока что в стадии заглушки.


class Stage(models.Model):
    name = models.CharField("Название этапа", default="Новый этап", max_length=50)
    data = models.OneToOneField(StageData, on_delete=models.CASCADE)
    parent = models.ForeignKey(Event, on_delete=models.CASCADE)


class StageRelation(models.Model):
    stage_from = models.OneToOneField(Stage, related_name="stage_from", on_delete=models.CASCADE)
    stage_to = models.OneToOneField(Stage, related_name="stage_to", on_delete=models.CASCADE)

class EventData:
    def __init__(self, information, preview, date, sub_events):
        self.information = information
        self.preview = preview
        self.date = date
        self.sub_events = sub_events


class Objects:
    def __init__(self, objects):
        self.all_objects = objects

    def all(self):
        return self.all_objects

    def get(self, id=0, name=0):
        if id:
            result = None
            for object in self.all_objects:
                if object['id'] == id:
                    result = object
                    break
        elif name:
            result = None
            for object in self.all_objects:
                if object['name'] == name:
                    result = object
                    break
        else:
            result = self.all_objects

        return result

# test_data = [
#     {
#         'id': 1,
#         'name': 'Стендап',
#         'data': EventData(
#             'Каждый вечер в барах и ресторанах в центре Москвы звучат лучшие шутки, а также новый материал комиков с ТНТ и других телевизионных стендап-проектов. Для тех, кто хочет услышать лучшие шутки стендаперов, — мероприятия с платным входом. Для тех, кто хочет услышать новые шутки одним из первых, — мероприятия с бесплатным входом, где оплачивается только минимальная сумма заказа вкусной еды и напитков. Ежедневные шоу поднимут настроение после работы, решат проблему с выбором места для свидания, дня рождения или корпоратива.',
#             'Каждый день в центре Москвы выступают опытные комики с телевидения и YouTube.', '12.34.4567',
#             [{'name', '1 часть'}, {'name': '2 часть'}])
#     }
# ]

class Event:
    objects = Objects(test_data)