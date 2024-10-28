from sched import scheduler

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .models import Newsletter, send_newsletter


def schedule_newsletter(newsletter):
    """Запланируйте отправку рассылки в зависимости от ее периодичности."""
    trigger = None
    if newsletter.periodicity == 'day':
        trigger = CronTrigger(hour='*', minute='0')  # Раз в день в полночь
    elif newsletter.periodicity == 'week':
        trigger = CronTrigger(day_of_week='mon', hour='0', minute='0')  # Раз в неделю по понедельникам в полночь
    elif newsletter.periodicity == 'month':
        trigger = CronTrigger(day='1', hour='0', minute='0')  # Раз в месяц в первый день в полночь

    if trigger:
        scheduler.add_job(send_newsletter, trigger, args=[newsletter], id=str(newsletter.id), replace_existing=True)


def start_scheduler():
    scheduler = BackgroundScheduler()
    newsletters = Newsletter.objects.filter(status='started')

    for newsletter in newsletters:
        schedule_newsletter(newsletter)

    scheduler.start()
