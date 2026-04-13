import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery(broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
app.conf.beat_schedule = {
     "weather_forecasts_update_task": {
         "task": "event_app.tasks.weather_forecasts_update_task",
         "schedule": crontab(minute="*/5"),
     },
    "check_event_statuses": {
        "task": "event_app.tasks.check_event_statuses",
        "schedule": crontab(minute="*/5"),
    },
}

@setup_logging.connect
def config_loggers(*args, **kwags) -> None:
    """Подключение логов в Celery."""
    from logging.config import dictConfig

    dictConfig(settings.LOGGING)


if __name__ == '__main__':
    app.start()
