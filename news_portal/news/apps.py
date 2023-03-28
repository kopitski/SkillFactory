from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'


class SubscriptionConfig(AppConfig):
    name = 'email'

    def ready(self):
        from .tasks import notify_weekly
        from .scheduler import subscription_scheduler

        import news.signals
        print('started')

        subscription_scheduler.add_job(
            id='notify weekly',
            func=notify_weekly,
            trigger='interval',
            seconds=10,
        )
        #subscription_scheduler.start()