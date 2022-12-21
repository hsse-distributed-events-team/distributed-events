from django.db import models


class StageSettings(models.Model):
    class AccessLevel(models.IntegerChoices):
        """
        Именованные константы для отображения уровня доступа к функциям настройки
        Можно расширить
        """
        STAFF = 5
        CURATOR = 10
        PROVIDER = 100

    can_user_choose_venue = models.BooleanField("Выбор площадки пользователем", default=False)
    application_auto_accept = models.BooleanField("Автопринятие заявок", default=False)
    public_participant_list = models.BooleanField("Публичный список участников", default=False)
    contacts_is_visible = models.BooleanField("Отображение контактов", default=False)
    who_can_edit_venues = models.SmallIntegerField("Кто может радактировать площадки", choices=AccessLevel.choices,
                                                   default=AccessLevel.PROVIDER)
    who_can_accept_applications = models.SmallIntegerField("Кто может принимать заявки", choices=AccessLevel.choices,
                                                           default=AccessLevel.PROVIDER)
    who_can_manage_mailing_list = models.SmallIntegerField("Кто может управлять рассылкой", choices=AccessLevel.choices,
                                                           default=AccessLevel.PROVIDER)

    def __str__(self):
        try:
            return str(self.stage)
        except:
            return f"Настройки лежат сами по себе. {self.id}"

    class Meta:
        """
        Настройка отображения в админ-панели
        """
        verbose_name = 'Настройки этапа'
        verbose_name_plural = 'Настройки этапа'
