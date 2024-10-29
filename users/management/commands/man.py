from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create manager user'

    def handle(self, *args, **options):
        User = get_user_model()

        # Создание группы менеджера
        moderator_group, created = Group.objects.get_or_create(name='manager')

        # Права
        permissions = [
            'can_change_newsletter_status',
            'can_change_user_status',
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                moderator_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {perm} does not exist.'))

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