from django.db.models import TextChoices, ForeignKey, CharField, CASCADE, RESTRICT, BooleanField, \
    PositiveSmallIntegerField

from app.models.driver.driver import Driver
from app.models.file import File
from django.utils.translation import gettext_lazy as _

from app.models.location.state import State


class Ticket(File):

    class TicketIssuer(TextChoices):
        DOT = 'DOT', _('Department of Transportation')
        POLICE = 'Police', _('Police')

    driver = ForeignKey(Driver, on_delete=CASCADE)
    issued_by = CharField(max_length=6, choices=TicketIssuer.choices, default=TicketIssuer.DOT)
    issue_state = ForeignKey(State, on_delete=RESTRICT)
    charged = BooleanField(default=False)
    amt = PositiveSmallIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.charged and self.amt:
            self.charged = True
        super(Ticket, self).save(args, kwargs)
