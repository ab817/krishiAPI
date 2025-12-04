from django.apps import AppConfig


class KrishiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'krishi'

    def ready(self):
        pass