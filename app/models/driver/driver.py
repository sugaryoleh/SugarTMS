from django.db.models import Model, TextChoices, AutoField, CharField, ForeignKey, RESTRICT, EmailField, \
    PositiveSmallIntegerField, BooleanField, TextField, SET_NULL, CASCADE, OneToOneField
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from app.models.driver.validators import validate_driver_license, validate_coordinator
from app.models.location.address import Address
from app.models.location.state import State
from app.models.parties.carriercompany import CarrierCompany
from app.models.unit.truck import Truck
from app.models.users.profile import Profile


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
    is_active = BooleanField(default=True)
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

    @staticmethod
    def get_last_unload_stage(driver):
        from app.models.load.load import Load
        loads = Load.objects.filter(driver=driver.id)
        if loads:
            last_stages = [Load.get_last_del_stage(load) for load in loads]

            def sort_key(e):
                return e.time_to

            last_stages.sort(reverse=True, key=sort_key)
            last_stage = last_stages[0]
            return last_stage
        return None

    @staticmethod
    def get_last_load(driver):
        last_stage = Driver.get_last_unload_stage(driver)
        if last_stage:
            from app.models.load.load import Load
            return Load.objects.get(pk=last_stage.load.id)
        return None
