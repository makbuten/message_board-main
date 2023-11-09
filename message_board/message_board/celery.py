import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_board.settings')

app = Celery('message_board')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Moscow'
app.conf.beat_schedule = {
    'every_week_notification':{
        'task': 'posts.tasks.weekly_notificator',
        'schedule': crontab(hour=20, minute=00, day_of_week='monday'),
        'args': (),
    }
}
app.autodiscover_tasks()
