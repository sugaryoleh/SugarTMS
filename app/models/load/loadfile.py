from django.db.models import TextChoices, CharField, ForeignKey, CASCADE

from app.models.file import File
from django.utils.translation import gettext_lazy as _

from app.models.load.load import Load


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
