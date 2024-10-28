from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create manager user'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='manager',
            first_name='manager',
            last_name='managerov',
            is_authenticated=True,
            is_staff=True,
            is_superuser=False,
        )

        user.set_password('1234')
        user.save()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created manager with email: {user.email}, password: 1234.'))