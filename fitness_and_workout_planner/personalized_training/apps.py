from django.apps import AppConfig


class PersonalizedTrainingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personalized_training'

    def ready(self):
        import personalized_training.signals
