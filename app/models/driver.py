from django.db.models import Model, TextChoices, AutoField, CharField, ForeignKey, RESTRICT, PositiveSmallIntegerField, \
    EmailField, BooleanField, TextField, SET_NULL, CASCADE, OneToOneField

from django.utils.translation import gettext_lazy as _

from app.models.address import Address, State
from phonenumber_field.modelfields import PhoneNumberField

from app.models.parties import CarrierCompany
from app.models.profile import Profile
from app.models.units import Truck
from app.models.validators import validate_driver_license, validate_coordinator


class Driver(Model):

    class HireType(TextChoices):
        FLAT_RATE = 'FR', _('Flat rate')
        CENT_PER_MILE = 'CPM', _('Cent per mile')
        OWNER = 'OWN', _('Owner')

    id = AutoField(primary_key=True)
    first_name = CharField(max_length=35)
    middle_name = CharField(max_length=35, null=True, blank=True)
    last_name = CharField(max_length=35)
    home_address = ForeignKey(Address, on_delete=RESTRICT)
    email = EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    license_number = CharField(max_length=10, validators=[validate_driver_license])
    license_state = ForeignKey(State, on_delete=RESTRICT)
    hire_type = CharField(max_length=3, choices=HireType.choices)
    pay = PositiveSmallIntegerField(null=True, blank=True)
    active = BooleanField(default=True)
    notes = TextField(max_length=200, null=True, blank=True)
    coordinator = ForeignKey(Profile, on_delete=SET_NULL, null=True, validators=[validate_coordinator])
    truck = OneToOneField(Truck, on_delete=RESTRICT, null=True, blank=True)
    company = ForeignKey(CarrierCompany, on_delete=CASCADE)

    class Meta:
        unique_together = ('license_number', 'license_state')

    def __str__(self):
        middle_name = ''
        if self.middle_name:
            middle_name = self.middle_name

        return '{} {} {}'.format(self.first_name, middle_name, self.last_name)