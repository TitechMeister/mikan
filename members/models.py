import io
import uuid
import PIL
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Section(models.Model):
    """
    A model represents section. (e.g. Bird, Econo, ...)
    """
    name = models.CharField(
        _('section name'),
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name


class Team(models.Model):
    """
    A model represents team. (e.g. Wing, Propeller, ...)
    """
    name = models.CharField(
        _('team name'),
        max_length=30,
        unique=True
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True
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

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    team = models.ForeignKey(Team, on_delete=models.SET_NULL,
                             blank=True, null=True)

    ja_last_name = models.CharField(
        _("First name (ja)"),
        max_length=16,
        blank=True,
        default="",
    )

    ja_first_name = models.CharField(
        _("Last name (ja)"),
        max_length=16,
        blank=True,
        default="",
    )

    felica_idm = models.CharField(
        _("felica IDm"),
        max_length=16,
        blank=True,
        default="",
    )

    executive_generation = models.PositiveSmallIntegerField(
        _("Executive generation"),
        null=True,
        blank=True,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )

    # upload path is defined in save()
    profile_image = models.ImageField(
        null=True,
        blank=True
    )

    def save(self, **kwargs):
        if self.profile_image:
            image = PIL.Image.open(self.profile_image)
            width, height = image.size
            size = min(width, height)
            image = image.crop(((width - size) // 2,
                                (height - size) // 2,
                                (width + size) // 2,
                                (height + size) // 2))

            image_io = io.BytesIO()
            image.save(image_io, format="PNG")

            imageName = f"images/{self.uid}.png"
            default_storage.delete(imageName)
            imageContent = ContentFile(image_io.getvalue(),
                                       name=imageName)
            self.profile_image.save(name=imageName,
                                    content=imageContent,
                                    save=False)

        super(Member, self).save(**kwargs)

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
