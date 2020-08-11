from cycle_mails.models import Crontab, SentDone
from django.utils import timezone
import datetime
import logging
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


def check_mails_tosend():
    now = timezone.now()

    # Check once send
    start_hour = datetime.time(now.hour, round((now.minute -5)/10)*10)
    end_hour = datetime.time(now.hour, round((now.minute +5)/10)*10)
    _once = Crontab.objects.filter(
        recurrence='O',
        week=now.weekday(),
        month=now.month,
        hour__gte=start_hour,
        hour__lte=end_hour,
    )
    for cron in _once:
        last_sent = SentDone.objects.filter(crontab=cron)
        if not last_sent:
            prepare_mail(cron)
        # We mail_queue the margin of 5 minutes of cron
        elif not (last_sent.minute > now.minute -5 and \
            last_sent.minute < now.minute +5):
            prepare_mail(cron)

    # Check weekly send
    _weekly = Crontab.objects.filter(
        recurrence='W',
        week=now.weekday(),
        hour__gte=start_hour,
        hour__lte=end_hour,
    )
    for cron in _weekly:
        last_sent = SentDone.objects.filter(crontab=cron)
        if not last_sent:
            prepare_mail(cron)
        # last sent past week. isocalendar gives week number in year
        elif last_sent.isocalendar()[1] < now.isocalendar()[1]:
            prepare_mail(cron)
        # last sent in last year (the week should be the same
        # as filter is week=now)
        elif last_sent.year < now.year:
            prepare_mail(cron)

    # Check monthly send
    _monthly = Crontab.objects.filter(
        recurrence='M',
        month=now.month,
        hour__gte=start_hour,
        hour__lte=end_hour,
    )
    for cron in _monthly:
        last_sent = SentDone.objects.filter(crontab=cron)
        if not last_sent:
            prepare_mail(cron)
        # last sent past month
        elif last_sent.month < now.month:
            prepare_mail(cron)
        # last sent in last year (the month should be the same
        # as filter is month=now)
        elif last_sent.year < now.year:
            prepare_mail(cron)


def prepare_mail(cron):
    logger.info("Sending mail for reunion <{}>...".format(cron.reunion))

    content = cron.reunion.content_set.all().first()

    emails = list(map(lambda e: e.name, cron.reunion.emails.all()))

    if content:
        send_mail(
            content.subject,
            content.body,
            'andujar@envios_reuniones.es',
            emails,
            fail_silently=False,
        )