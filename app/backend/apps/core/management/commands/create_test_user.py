"""
テストユーザーを作成するコマンド
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'テストユーザーを作成します'

    def handle(self, *args, **options):
        username = 'testuser'
        password = 'testpass123'
        email = 'test@example.com'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'ユーザー "{username}" は既に存在します')
            )
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'テストユーザーを作成しました: {username} / {password}'
            )
        )

