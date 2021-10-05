from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self) -> None:
        """Call all signals to execute"""
        import user.api.signals
