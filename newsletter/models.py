from django.db import models
from django.utils import timezone

from newsletter.utils import should_run_task


class User(models.Model):
    '''Модель пользователя представляет собой контактные данные о человеке, который должен будет получить сообщение'''
    full_name = models.CharField(
        max_length=50,
        verbose_name='ФИО Пользователя',
        help_text='Введите полное имя пользователя', )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )

    def __str__(self):
        return (f'{self.name} ({self.email})')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Company(models.Model):
    '''Модель компании сделана исключительно в индивидуальных целях и далее будет дополняться.
    в этой модели создается название организации для дальнейшей фильтрации (если клиентов из данной организации будет
    не 1 а более'''
    name = models.CharField(
        max_length=50,
        verbose_name='название организации',
    )
    link = models.CharField(
        max_length=50,
        verbose_name='сайт компании',
        blank=True,
        null=True
    )

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'


class Client(models.Model):
    '''Модель клиента содержит в себе ФИО клиента, почту, компанию и комментарий'''
    full_name = models.CharField(
        max_length=50,
        verbose_name='фио клиента',
        help_text='Введите полное имя клиента'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='компания',
        help_text='Введите название организации'
    )
    comment = models.TextField(
        verbose_name='комментарий'
    )

    def __str__(self):
        return (f'{self.name} ({self.email}\n{self.comment})')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


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
