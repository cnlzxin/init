from app import celery
from celery.schedules import crontab

CALCULATE_QUEUE_NAME = 'calculate.something'


@celery.on_after_configure.connect
def setup_calculate_periodic_tasks(sender, **kwargs):
    """ 定时任务, 周期性运行 """
    sender.add_periodic_task(
        crontab(minute='*/1'),
        add.s(1, 2),
        name='calculate-something',
    )


@celery.task(queue=CALCULATE_QUEUE_NAME)
def add(x, y):
    return x + y
