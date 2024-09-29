from django.apps import AppConfig

class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'


class NewsletterAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()
