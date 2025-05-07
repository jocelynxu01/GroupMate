from django.apps import AppConfig


class GroupmateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'groupmate'

    def ready(self):
        import groupmate.signals
