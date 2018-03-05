from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
import uuid


class Team(models.Model):
    """
    A model represents team. (e.g. Wing, Propeller, ...)
    """
    name = models.CharField(
        _('team name'),
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name


class Member(AbstractUser):
    """
    A model represents member.
    First name, last name, email are provided by AbstractUser.
    """
    uid = models.UUIDField(default=uuid.uuid4,
                           null=False,
                           editable=False)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL,
                             blank=True, null=True)

    felica_idm = models.CharField(
        _("felica IDm"),
        max_length=16,
        blank=True,
        default="",
    )

    exective_generation = models.PositiveSmallIntegerField(
        _("Executive generation"),
        null=True,
        blank=True,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )

    profile_image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
