from django.db import models
from django.contrib.auth.models import User as DjangoUser


class PersonalData(models.Model):
    name = models.CharField('Имя', max_length=20)
    surname = models.CharField('Фамилия', max_length=20)
    # Пока что в стадии заглушки. Возможно расширить без ущерба для производства


# Create your models here.
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
