from config.settings import EMAIL_HOST_USER

from django.utils import timezone
from django.core.mail import send_mail
from newsletter.models import Newsletter, NewsletterAttempt


def send_newsletters():
    now = timezone.now()
    newsletters = Newsletter.objects.filter(
        scheduled_at__lte=now,
        status='started'
    )

    for newsletter in newsletters:
        # Логика отправки рассылки
        try:
            # Здесь вы должны указать, как отправить сообщения
            # Например, если у вас есть список клиентов
            for client in newsletter.clients.all():
                send_mail(
                    newsletter.message.title,
                    newsletter.message.message,
                    EMAIL_HOST_USER,
                    [client.email],
                )

            # Запись попытки рассылки
            NewsletterAttempt.objects.create(
                newsletter=newsletter,
                status='success'
            )

            # Обновляем дату последней отправки
            newsletter.last_run = now
            newsletter.save()

            # Проверяем периодичность
            if newsletter.periodicity == 'day':
                newsletter.scheduled_at += timezone.timedelta(days=1)
            elif newsletter.periodicity == 'week':
                newsletter.scheduled_at += timezone.timedelta(weeks=1)
            elif newsletter.periodicity == 'month':
                newsletter.scheduled_at += timezone.timedelta(weeks=4)

            # Если запланирована новая отправка, сохраняем статус как 'started'
            newsletter.status = 'started'  # можно оставить или изменить статус по вашему желанию
            newsletter.save()

        except Exception as e:
            # Если произошла ошибка, записываем это в попытку рассылки
            NewsletterAttempt.objects.create(
                newsletter=newsletter,
                status='failure',
                server_response=str(e)
            )

