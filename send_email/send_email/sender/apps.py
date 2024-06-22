from django.apps import AppConfig


class SenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'send_email.sender'
