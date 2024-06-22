from django.apps import AppConfig


class WebsocketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_management.websocket'

    def ready(self):
        import project_management.websocket.signals