import pytz
from string import ascii_letters, digits
from random import choices
from datetime import timedelta
from django.db import models
from django.utils import timezone
from members.models import Member

# Create your models here.


def generate_code():
    return "".join(choices(ascii_letters + digits, k=30))


def generate_24h_after():
    return timezone.now() + timedelta(days=1)


class RecoverToken(models.Model):
    token = models.CharField(max_length=30,
                             default=generate_code,
                             unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    valid_until = models.DateTimeField(default=generate_24h_after)

    def __str__(self):
        tz = pytz.timezone('Asia/Tokyo')
        if (self.valid_until):
            valid_until = self.valid_until.astimezone(tz).strftime('%x %X')
        else:
            valid_until = "(no time limit)"
        return (f"{str(self.token)} - {valid_until}")
