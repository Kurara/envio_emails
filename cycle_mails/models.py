from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Reunion(models.Model):
    """ Reunions to program email send to

    """
    name = models.CharField(max_length=200)
    emails = models.ManyToManyField('Recipient')

    def __str__(self):
        return "{}".format(self.name)


class Recipient(models.Model):
    """ Recipient 
    """
    email = models.EmailField(max_length=200)

    def __str__(self):
        return "{}".format(self.email)


class Content(models.Model):
    """ The body of the message to send
    """
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    
    def __str__(self):
        return _("Content for {}").format(self.reunion.name)

class Crontab(models.Model):
    """ The crontab to send mails
    """

    RECURENCE_CHOICES = (
        ('W', _("Weekly")),
        ('M', _("Monthly")),
        ('O', _("Once")),
    )
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    recurrence = models.CharField(
        choices=RECURENCE_CHOICES,
        default='O',
        max_length=1
    )
    hour = models.TimeField()
    week = models.IntegerField(
        choices=(
            (1, _("Monday")),
            (2, _("Tuesday")),
            (3, _("Wednesday")),
            (4, _("Thursday")),
            (5, _("Friday")),
            (6, _("Saturday")),
            (7, _("Sunday"))
        ),
        null=True,
        blank=True
    )
    month = models.IntegerField(
        choices=(
            (1, _("January")),
            (2, _("February")),
            (3, _("March")),
            (4, _("April")),
            (5, _("May")),
            (6, _("June")),
            (7, _("July")),
            (8, _("August")),
            (9, _("September")),
            (10, _("October")),
            (11, _("November")),
            (12, _("December")),
        ),
        null=True,
        blank=True
    )

    def __str__(self):
        current_recurrence = list(filter(
            lambda r: r[0] == self.recurrence,
            self.RECURENCE_CHOICES.__iter__()
        ))
        recurence_str = current_recurrence[0][1]
        return _("<{}>:{}").format(recurence_str, self.hour)

class SentDone(models.Model):
    """ The list of emails sent
    """
    crontab = models.ForeignKey(Crontab, on_delete=models.CASCADE)
    last_sent = models.DateTimeField()