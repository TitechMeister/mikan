import pytz
from django.db import models
from django.utils.translation import ugettext_lazy as _
from members.models import Member


class Workplace(models.Model):
    """
    A model represents a place to work.
    """
    name = models.CharField(
        _('workplace name'),
        max_length=30,
        unique=True
    )

    color = models.CharField(
        _('color code(hex)'),
        max_length=7,
        default='#fda313'
    )

    danger = models.BooleanField(
        _('danger'),
        default=False
    )

    def __str__(self):
        return self.name


class Work(models.Model):
    """
    A model represents history of work.
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, default=1,
                                  on_delete=models.SET_DEFAULT)
    start_at = models.DateTimeField(
        _("start at"),
        null=True,
        blank=False,
    )
    end_at = models.DateTimeField(
        _("end at"),
        null=True,
        blank=True,
    )
    is_just_staying = models.BooleanField(
        _("just staying"),
        default=False
    )

    def __str__(self):
        tz = pytz.timezone('Asia/Tokyo')
        start = self.start_at.astimezone(tz).strftime('%x %X')
        if self.end_at:
            end = self.end_at.astimezone(tz).strftime('%x %X')
        else:
            end = ">"
        return (f"{str(self.member)} @ {str(self.workplace)}"
                + f" : {start} - {end}")

    class Meta:
        permissions = (
            ("create_work_universally", "Can create work universally"),
        )
