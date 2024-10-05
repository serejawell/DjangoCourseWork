from django.core.management.base import BaseCommand
from django.utils import timezone
from newsletter.models import Newsletter

class Command(BaseCommand):
    help = 'Отправляет рассылки'

    def handle(self, *args, **kwargs):
        newsletters = Newsletter.objects.filter(status='started', scheduled_at__lte=timezone.now())

        for newsletter in newsletters:
            if newsletter.can_send():  # Здесь можно добавить логику отправки
                # Логика отправки сообщения
                # Например:
                # send_email_to_clients(newsletter)
                newsletter.status = 'completed'
                newsletter.last_run = timezone.now()
                newsletter.save()
                self.stdout.write(self.style.SUCCESS(f'Рассылка {newsletter.message.title} успешно отправлена!'))
            else:
                self.stdout.write(self.style.WARNING(f'Рассылка {newsletter.message.title} не может быть отправлена.'))
