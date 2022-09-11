import os

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
from django.apps import apps

from core.celery.logger import TaskJSONStructuredFormatter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
app = Celery("bakersoft")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(
    lambda: [django_app.name for django_app in apps.get_app_configs()]
)


@after_setup_task_logger.connect
def after_setup_task_logger_receiver(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(TaskJSONStructuredFormatter())


@after_setup_logger.connect
def after_setup_logger_receiver(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(TaskJSONStructuredFormatter())
