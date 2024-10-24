from datetime import timedelta
from django.utils import timezone


def should_run_task(last_run, periodicity):
    now = timezone.now()

    if periodicity == 'day':
        return now >= last_run + timedelta(days=1)
    elif periodicity == 'week':
        return now >= last_run + timedelta(weeks=1)
    elif periodicity == 'month':
        return now >= last_run + timedelta(days=30)

    return False