from django.db import models
from user_handler.models import User


class EventData(models.Model):
    data = models.TextField(null=True, blank=True, max_length=500)
    # Пока что в ставдии заглушки.


class Event(models.Model):
    name = models.CharField("Название мероприятия", default="Новое мероприятие", max_length=50)
    data = models.OneToOneField(EventData, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through="Application")


class Application(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update_time = models.DateTimeField()
    status = models.IntegerField("Код статуса заявки")  # Пока что пусть код статуса будет числом, что мы преобразуем
    result = models.TextField("Результат события", max_length=500)  # Пусть пока что результат будет длинной строкой



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
