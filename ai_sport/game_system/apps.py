from django.apps import AppConfig


class GameSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game_system'
    verbose_name = '游戏化系统'

    def ready(self):
        import game_system.signals
