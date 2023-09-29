import json
from django.utils import timezone
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import requests
from config.settings import TELEGRAM_BOT_API_KEY
from atomic_habits.models import Habit


@shared_task
def send_telegram_notification(telegram_user_id, notification: str) -> None:
    """ Отправляет уведомления в Telegram """

    base_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/'
    user_id = telegram_user_id
    params = {'chat_id': user_id, 'text': notification}
    response = requests.post(base_url + 'sendMessage', params=params)


@shared_task
def create_periodic_task(habit_pk: int):
    """ При создании новой привычки создает отложенную задачу для отправки уведомления через Telegram """

    habit = Habit.objects.filter(pk=habit_pk).first()
    notification_to_send = f'Напоминание: {habit.action} не меньше {habit.time_to_complete} секунд.'
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.periodicity,
        period=IntervalSchedule.DAYS
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name=habit.action,
        start_time=timezone.now(),
        task='atomic_habits.tasks.send_telegram_notification',
        args=json.dumps([habit.user.telegram_id, notification_to_send])
    )
