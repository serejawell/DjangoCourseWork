from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Модель пользователя (тот, кто отправляет рассылку) содержит в себе ФИО, почту'''

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="email",
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя пользоватея',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия пользователя',
    )
    avatar = models.ImageField(
        upload_to='users/avatars',
        blank=True,
        null=True,
        verbose_name='аватар'
    )
    phone = models.CharField(
        max_length=35,
        verbose_name='Номер телефона',
        blank=True,
        null=True
    )
    token = models.CharField(
            max_length=100,
            verbose_name='токен',
            blank=True,
            null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_change_user_status','Can activate/deactivate user'),
        ]

    def __str__(self):
        return self.email
