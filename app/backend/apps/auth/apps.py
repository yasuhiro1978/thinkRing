from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth'
    label = 'custom_auth'  # django.contrib.authとの衝突を回避
    verbose_name = '認証'

