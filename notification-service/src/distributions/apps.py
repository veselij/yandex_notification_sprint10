from django.apps import AppConfig


class DistributionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "distributions"

    def ready(self):
        import distributions.signals
