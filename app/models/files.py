from django.core.exceptions import ValidationError
from django.db.models import Model, AutoField, CharField, FileField, ForeignKey, CASCADE, TextChoices, RESTRICT, \
    PositiveSmallIntegerField, SET_NULL, BooleanField
from django.utils.translation import gettext_lazy as _

from app.models.address import State
from app.models.driver import Driver
from app.models.load import Load
from app.models.units import Trailer, Truck
from app.models.profile import Profile


def get_file_path(instance, filename):
    folder = ''
    if instance.__class__ == DriverFile:
        folder = 'drivers/{}/'.format(instance.driver.id)
    elif instance.__class__ == TruckFile:
        folder = 'trucks/{}/'.format(instance.truck.id)
    elif instance.__class__ == TrailerFile:
        folder = 'trailers/{}/'.format(instance.trailer.id)
    elif instance.__class__ == LoadFile:
        folder = 'loads/{}/'.format(instance.trailer.id)
    path = 'files/{}/{}'.format(folder, filename)
    return path


class File(Model):
    id = AutoField(primary_key=True)
    file = FileField(upload_to=get_file_path)
    notes = CharField(max_length=20, null=True, blank=True)
    added_by = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=True)


class DriverFile(File):
    driver = ForeignKey(Driver, on_delete=CASCADE)


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


class TrailerFile(File):
    trailer = ForeignKey(Trailer, on_delete=CASCADE)


class TruckFile(File):
    truck = ForeignKey(Truck, on_delete=CASCADE)


class LoadFile(File):
    class FileType(TextChoices):
        RC = 'RC', _('Rate confirmation')
        RECEIPT = 'RECEIPT', _('Receipt')
        BOL = 'BOL', _('Bill of landing')
        PDO = 'POD', _('Proof of delivery')
        INVOICE = 'INVOICE', _('Invoice')

    type = CharField(max_length=7, choices=FileType.choices, null=True, blank=True)
    load = ForeignKey(Load, on_delete=CASCADE)

    def __str__(self):
        return '{} {}'.format(self.load, self.type)