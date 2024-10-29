from config.settings import EMAIL_HOST_USER

from django.utils import timezone
from django.core.management.base import BaseCommand
from newsletter.models import Newsletter, NewsletterAttempt
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Send scheduled newsletters'

    def handle(self, *args, **options):
        now = timezone.now()
        newsletters = Newsletter.objects.filter(
            scheduled_at__lte=now,
            status__in=['created', 'started']  # Проверка на статус "Создана" или "Запущена"
        )

        for newsletter in newsletters:
            # Изменяем статус на "Запущена", если он "Создана"
            if newsletter.status == 'created':
                newsletter.status = 'started'
                newsletter.save()

            clients = newsletter.clients.all()  # Получаем клиентов для этой рассылки
            message = newsletter.message.message  # Предполагается, что у вас есть поле 'content' в модели Message

            # Отправка email
            for client in clients:
                send_mail(
                    subject=newsletter.message.title,
                    message=message,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[client.email],
                )

            # Создание записи о попытке рассылки
            NewsletterAttempt.objects.create(
                newsletter=newsletter,
                attempt_date=timezone.now(),
                status='success',  # Укажите статус попытки
                server_response='Emails sent successfully'
            )

            # Обновление поля last_run
            newsletter.last_run = now
            newsletter.save()

            # Если периодичность - "раз в день", то нужно обновить scheduled_at для следующей отправки
            if newsletter.periodicity == 'day':
                newsletter.scheduled_at += timezone.timedelta(days=1)
            elif newsletter.periodicity == 'week':
                newsletter.scheduled_at += timezone.timedelta(weeks=1)
            elif newsletter.periodicity == 'month':
                newsletter.scheduled_at += timezone.timedelta(weeks=4)

            newsletter.save()  # Сохраняем обновления
