from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create user'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='user',
            first_name='User',
            last_name='Userov',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('1234')
        user.save()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created user with email: {user.email} password: 1234.'))
