from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('1234')
        user.save()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created superuser with email: {user.email}, password: 1234.'))