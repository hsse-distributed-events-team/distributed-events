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
