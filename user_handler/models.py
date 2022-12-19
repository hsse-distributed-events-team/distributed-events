from django.db import models
from django.contrib.auth.models import User as DjangoUser


class PersonalData(models.Model):
    name = models.CharField('Имя', max_length=20)
    surname = models.CharField('Фамилия', max_length=20)
    region = models.SmallIntegerField('Регион', default=1)
    # Пока что в стадии заглушки. Возможно расширить без ущерба для производства

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name="django_user")
    personal_data = models.OneToOneField(PersonalData, on_delete=models.CASCADE)
    is_verified = models.BooleanField('Проверенный пользователь', default=False)

    class Meta:
        """
        Настройка отображения в админ-панели
        """
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.user.username} User'
