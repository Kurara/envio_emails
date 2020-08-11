from django.test import TestCase
import logging
from cycle_mails.cron import check_mails_tosend
from cycle_mails.models import Crontab, Reunion
from django.utils import timezone


logger = logging.getLogger(__name__)


class CycleTestCase(TestCase):

    def setUp(self):
        self.reunion = Reunion.objects.create(
            name='Example reunion',
        )

    def test_check_mails_tosend(self):
        check_mails_tosend()

    def test_check_mails_tosend_week(self):
        Crontab.objects.create(
            week=timezone.now().weekday(),
            reunion=self.reunion,
            hour="{}:{}".format(
                timezone.now().hour,
                timezone.now().minute
            ),
            recurrence='W'
        )
        check_mails_tosend()

    def test_check_mails_tosend_month(self):
        Crontab.objects.create(
            month=timezone.now().month,
            reunion=self.reunion,
            hour="{}:{}".format(
                timezone.now().hour,
                timezone.now().minute
            ),
            recurrence='M'
        )
        check_mails_tosend()

    def test_check_mails_tosend_once(self):
        Crontab.objects.create(
            week=timezone.now().weekday(),
            month=timezone.now().month,
            reunion=self.reunion,
            hour="{}:{}".format(
                timezone.now().hour,
                timezone.now().minute
            ),
            recurrence='O'
        )

        check_mails_tosend()

    def tearDown(self):
        # Restores backup image
        pass
