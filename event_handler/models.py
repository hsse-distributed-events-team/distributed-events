from django.db import models
from user_handler.models import User

class Event(models.Model):

    """
    Класс **Event**

    :param name: название мероприятия
    :param description: информация о мероприятии

    """

    name = models.CharField("Название мероприятия", default="Новое мероприятие", max_length=50)
    description = models.TextField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        """
        Настройка отображения в админпанели
        """
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['name']


class Stage(models.Model):
    """
    Класс **Stage**

    :param name: название этапа
    :param description: описание этапа
    :param parent: родитель
    :param preview: превью
    :param users: участники
    :param status: статус
    :param time_start: начало
    :param time_end: конец

    """
    class Status(models.IntegerChoices):
        """
        Именованные константы, отображающие статус этапа мероприятия
        Можно расширить

        :param WAITING: 0
        :param ACTIVE: 1
        :param ENDED: 2

        """
        WAITING = 0
        ACTIVE = 1
        ENDED = 2

    name = models.CharField("Название этапа", default="Новый этап", max_length=50)
    parent = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, max_length=500)
    preview = models.TextField(null=True, blank=True, max_length=100)
    users = models.ManyToManyField(User, through="Application")
    status = models.SmallIntegerField(null=True, default=Status.WAITING, choices=Status.choices)
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        """
        Настройка отображения в админ-панели
        """
        verbose_name = 'Этап'
        verbose_name_plural = 'Этапы'
        ordering = ['name']


class StageRelation(models.Model):
    stage_from = models.OneToOneField(Stage, related_name="stage_from", on_delete=models.CASCADE)
    stage_to = models.OneToOneField(Stage, related_name="stage_to", on_delete=models.CASCADE)


class Venue(models.Model):
    """
    Класс **Venue**

    :param name: название этапа
    :param address: адрес проведения

    """
    name = models.CharField("Название", max_length=50)
    address = models.TextField("Адрес", max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        """
        Настройка отображения в админ-панели
        """
        verbose_name = 'Площадка проведения'
        verbose_name_plural = 'Площадки проведения'
        ordering = ['name']


class Application(models.Model):
    class Status(models.IntegerChoices):
        """
        Именованные константы для отображения статуса заявки(участия) в мероприятии
        Можно расширить
        """
        AWAITED = 0
        ACCEPTED = 200
        REJECTED = 400
        BANNED = 404

    class Roles(models.IntegerChoices):
        """
        Именованные константы для отображеня роли учатися в мероприятии
        Можно расширить
        """
        PARTICIPANT = 0
        STAFF = 1
        ADMIN = 100
    """
    Класс **Application**

    :param stage: Stage
    :param user: User
    :param venue: Venue
    :param role: Роль
    :param last_update_time: время последнего обновления
    :param status: Статус заявки
    :param result: Результат события

    """
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    role = models.SmallIntegerField("Роль", choices=Roles.choices, default=Roles.PARTICIPANT)
    last_update_time = models.DateTimeField()
    status = models.SmallIntegerField("Статус заявки", default=Status.AWAITED)
    result = models.TextField("Результат события", max_length=500)  # Пусть пока что результат будет длинной строкой
