from django.apps import AppConfig


class EducationPlatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education_platform'

    verbose_name = 'Образовательная платформа'

    def ready(self):
        import education_platform.signals
