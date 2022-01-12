from django.apps import AppConfig


class TimonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timon'

    def ready(self):
        import timon.terraform  # noqa
