from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Model, AutoField, CharField, ForeignKey, RESTRICT, BooleanField, UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _

from app.models.address import Address
from app.models.validators import validate_MC_number, validate_DOT_number, validate_logistics_company_rate


class LogisticsCompany(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True)
    address = ForeignKey(Address, on_delete=RESTRICT)
    MC = CharField(max_length=6, validators=[validate_MC_number], unique=True)
    DOT = CharField(max_length=7, validators=[validate_DOT_number], unique=True)
    rate = CharField(max_length=1, validators=[validate_logistics_company_rate])

    def __str__(self):
        return '{}'.format(self.name)


class BrokerCompany(LogisticsCompany):
    pass


class CarrierCompany(LogisticsCompany):
    is_main = BooleanField(default=False)

    def just_created(self):
        return not CarrierCompany.objects.filter(pk=self.pk).exists()

    def is_main_changed(self):
        if not self.just_created():
            return self.is_main != CarrierCompany.objects.get(pk=self.id).is_main

    @staticmethod
    def is_first():
        return not CarrierCompany.objects.all().exists()

    def save(self, *args, **kwargs):
        if self.is_first() and not self.is_main:
            raise Exception(_('The main Carrier Company must be created first'))
        elif (self.is_main and self.just_created()) or self.is_main_changed():
            raise Exception(_('The main Carrier Company must be set once'))
        super(LogisticsCompany, self).save(args, kwargs)
