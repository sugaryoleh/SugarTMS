from django.db.models import Model, AutoField, CharField, ForeignKey, RESTRICT, BooleanField

from app.models.location.address import Address
from app.models.parties.validators import validate_MC_number, validate_DOT_number, validate_logistics_company_rate


class LogisticsCompany(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True)
    address = ForeignKey(Address, on_delete=RESTRICT)
    MC = CharField(max_length=6, validators=[validate_MC_number], unique=True)
    DOT = CharField(max_length=7, validators=[validate_DOT_number], unique=True)
    rate = CharField(max_length=1, validators=[validate_logistics_company_rate])

    def __str__(self):
        return '{}'.format(self.name)
