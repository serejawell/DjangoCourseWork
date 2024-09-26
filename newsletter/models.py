from django.db import models
from django.utils import timezone

from newsletter.utils import should_run_task


class Client(models.Model):
    '''Модель клиента представляет собой контактные данные о человеке, который должен будет отправлять рассылки'''
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя клиента',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия клиента',
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name='Отчество клиента',
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    comment = models.TextField(
        verbose_name='комментарий',
        blank=True,
        null=True
    )

    def __str__(self):
        return (f'{self.last_name} {self.first_name} {self.middle_name} ({self.email})\n{self.comment}')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class User(models.Model):
    '''Модель пользователя содержит в себе ФИО, почту'''
    first_name = models.CharField(
        max_length=50,
        verbose_name='фио пользоватея',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия пользователя',
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name='Отчество пользователя',
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )

    def __str__(self):
        return (f'{self.last_name} {self.name} {self.middle_name} ({self.email})')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Message(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='тема сообщения'
    )
    message = models.TextField(
        verbose_name='введите сообщение'
    )

    def __str__(self):
        return (f'{self.title}\n{self.message}')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщении'


class Newsletter(models.Model):
    '''Создаем модель рассылки, в которой у нас будет дата и время первой отправки рассылки
    периодичность, статус'''
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    PERIOD_CHOICES = [
        ('day', 'Раз в день'),
        ('week', 'Раз в неделю'),
        ('month', 'Раз в месяц'),
    ]
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    scheduled_at = models.DateTimeField(
        verbose_name='Дата отправки'
    )

    periodicity = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES
    )
    last_run = models.DateTimeField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created'
    )

    def __str__(self):
        return (f'ID: {self.id} Дата отправки: {self.scheduled_at} Статуc: {self.status}')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def should_run(self):
        '''Функция позволяет запускать рассылку с переодичностью в день\неделю\месяц'''
        if self.last_run:
            return should_run_task(self.last_run, self.periodicity)
        return True

    def can_send(self):
        '''Функция позволяет проверить актуальность даты. Отправляет, если выбранная дата не в прошлом.'''
        if self.scheduled_at > timezone.now() and self.status == 'created':
            return True
        return False
