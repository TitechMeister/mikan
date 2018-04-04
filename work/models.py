import pytz
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from members.models import Member, Team, Section


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


class Activity(models.Model):
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
            ("create_activities_universally",
             "Can create activities universally"),
        )


class Work(models.Model):
    """
    A model represents work.
    """
    name = models.CharField(
        _('work name'),
        max_length=256,
        unique=True
    )
    assigned_team = models.ManyToManyField(
        Team,
        blank=True,
        help_text=_("Team(s) to assign this work. "
                    "More than one teams or sections should be assigned.")
    )
    assigned_section = models.ManyToManyField(
        Section,
        blank=True,
        help_text=_("Section(s) to assign this work. "
                    "More than one teams or sections should be assigned.")
    )
    description = models.TextField(
        help_text=_('Brief description for work.'),
        blank=True,
    )
    work_manual_url = models.URLField(
        help_text=_('Wiki page for work manual.'),
        blank=True,
    )
    default_workplace = models.ForeignKey(
        Workplace,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    @property
    def assigned(self):
        return ", ".join([x.name for x in self.assigned_section.all()]
                         + [x.name for x in self.assigned_team.all()])

    def __str__(self):
        return f"{self.name} - {self.assigned}"


class WorkPlan(models.Model):
    date = models.DateField(default=now)
    completed_by = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="workplan_completed"
    )
    work = models.ManyToManyField(
        Work,
        through="PracticalWork",
        help_text=_("Work to execture in this work plan. Required.")
    )
    assigned_team = models.ManyToManyField(
        Team,
        blank=True,
        help_text=_("Team(s) to assign this work plan. "
                    "If no team or section is assigned, "
                    "default of each work will be used.")
    )
    assigned_section = models.ManyToManyField(
        Section,
        blank=True,
        help_text=_("Section(s) to assign this work plan."
                    "If no team or section is assigned, "
                    "default of each work will be used.")
    )
    members = models.ManyToManyField(
        Member,
        blank=True,
        related_name="workplan_assigned",
        help_text=_("Member(s) to work on this work plan."
                    "If no member is assigned, "
                    "all members in assigned teams or sections will be used.")
    )

    @property
    def assigned(self):
        return ", ".join([x.name for x in self.assigned_section.all()]
                         + [x.name for x in self.assigned_team.all()])

    def __str__(self):
        return f"{self.date} - {self.assigned}"


class PracticalWork(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    workplan = models.ForeignKey(WorkPlan, on_delete=models.CASCADE)
    workplace = models.ForeignKey(
        Workplace,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Change this to override default workplace. "
                    "Leave it blank to use default.")
    )

# class WorkReport(models.Model):
#     date = models.DateField(default=now)
#     completed_by = models.ForeignKey(Member, on_delete=models.CASCADE)
