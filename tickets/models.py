from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
import datetime

# Create your models here.
class Tickets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("ticketed_user"), on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=32, unique=True, verbose_name="ticket_number")
    ticket_date = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return self.ticket_number

    class Meta:
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")