import logging

logger = logging.getLogger(__name__)

purge_queue = {"queue": "celery"}
uncategorized_queue = {"queue": "uncategorized"}
keep_queue = {"queue": "keep"}

router = {
    "celery.backend_cleanup": keep_queue,
    "work_tracking.tasks.notify_team_leaders_about_tasks_overdue_soon": purge_queue,
}


def task_router(name, args, kwargs, options, task=None, **kw):
    try:
        return router[name]
    except KeyError:
        logger.error(
            "Task %s has not been routed! Please add it to the `config.celery.task_router`.",
            name,
        )
    return uncategorized_queue
