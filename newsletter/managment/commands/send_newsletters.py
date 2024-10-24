from django.core.management.base import BaseCommand
from django.utils import timezone
from newsletter.models import Newsletter
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send newsletters to clients'

    def handle(self, *args, **kwargs):
        newsletters = Newsletter.objects.filter(status='created', scheduled_at__lte=timezone.now())
        for newsletter in newsletters:
            if newsletter.can_send():
                # Получаем список email адресов клиентов
                client_emails = newsletter.clients.values_list('email', flat=True)
                # Отправляем email
                for email in client_emails:
                    send_mail(
                        newsletter.message.title,
                        newsletter.message.message,
                        'from@example.com',  # Отправитель
                        [email],
                    )
                # Обновляем статус рассылки
                newsletter.status = 'completed'
                newsletter.last_run = timezone.now()
                newsletter.save()

                self.stdout.write(self.style.SUCCESS(f'Sent newsletter ID: {newsletter.id}'))
