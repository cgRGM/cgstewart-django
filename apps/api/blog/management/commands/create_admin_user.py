from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create a superuser for the Django admin using Pulumi-managed credentials'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username (overrides env var)')
        parser.add_argument('--email', type=str, help='Admin email (overrides env var)')
        parser.add_argument('--password', type=str, help='Admin password (overrides env var)')

    def handle(self, *args, **options):
        # Get credentials from environment variables (set by Pulumi) or command line args
        username = options.get('username') or os.environ.get('DJANGO_ADMIN_NAME', 'admin')
        email = options.get('email') or os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@cgstewart.com')
        password = options.get('password') or os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin123!')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser "{username}"')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write('Password: [HIDDEN FOR SECURITY]')
