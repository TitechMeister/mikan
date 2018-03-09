import pytz
from string import ascii_lowercase, digits
from random import choices
from django.db import models


def generate_code():
    return "".join(choices(ascii_lowercase + digits, k=10))


class RegistrationCode(models.Model):
    code = models.CharField(max_length=10,
                            default=generate_code,
                            unique=True)
    onetime = models.BooleanField(default=True)
    valid_until = models.DateTimeField(blank=True,
                                       null=True)

    def __str__(self):
        tz = pytz.timezone('Asia/Tokyo')
        if (self.valid_until):
            valid_until = self.valid_until.astimezone(tz).strftime('%x %X')
        else:
            valid_until = "(no time limit)"
        return (f"{str(self.code)} - {valid_until}"
                f"{'' if self.onetime else ' (super code)'}")
