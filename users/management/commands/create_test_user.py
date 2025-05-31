# users/management/commands/create_test_user.py

from django.core.management.base import BaseCommand, CommandError
from users.models import User # Импортируем нашу модель пользователя

class Command(BaseCommand):
    help = 'Creates a test user with a specified email and password, bypassing password validators.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email for the test user.')
        parser.add_argument('password', type=str, help='Password for the test user.')
        parser.add_argument('--is_staff', action='store_true', help='Set user as staff.')
        parser.add_argument('--is_superuser', action='store_true', help='Set user as superuser.')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        is_staff = options['is_staff']
        is_superuser = options['is_superuser']

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User with email "{email}" already exists.'))
            return

        try:
            user = User.objects.create_user(email=email, password=password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created test user: {email}'))
            if is_staff:
                self.stdout.write(self.style.SUCCESS(f'User {email} is now staff.'))
            if is_superuser:
                self.stdout.write(self.style.SUCCESS(f'User {email} is now superuser.'))

        except Exception as e:
            raise CommandError(f'Error creating user "{email}": {e}')