from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, verbose_name='Имя')
    email = models.EmailField()
    register = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Отправлять уведомления?')

    class Meta(AbstractUser.Meta):
        pass


class Book(models.Model):
    title = models.CharField(max_length=20, unique=False)
    author = models.ForeignKey(AdvUser, verbose_name='Автор', on_delete=models.SET_NULL, null=True, blank=True)
    year_of_publication = models.DateTimeField(verbose_name='Год издания')
    isbn = models.CharField(max_length=13, verbose_name='Международный книжный номер')
