from django.apps import AppConfig


class TrainingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training'

    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError
        try:
            from .seed import seed_training_plans, seed_achievements
            from .models import TrainingPlan
            if TrainingPlan.objects.count() == 0:
                seed_training_plans()
                seed_achievements()
        except (OperationalError, ProgrammingError):
            pass
