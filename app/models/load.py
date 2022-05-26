from django.db.models import Model, BigAutoField, BooleanField, ForeignKey, CASCADE, PositiveSmallIntegerField, \
    DateTimeField, RESTRICT, TextField, CharField, AutoField, TextChoices
from django.utils.translation import gettext_lazy as _

from app.models.driver import Driver
from app.models.facility import Facility
from app.models.parties import BrokerCompany, CarrierCompany
from app.models.profile import Profile
from app.models.units import Trailer
from app.models.validators import validate_coordinator, driver_for_load_validator
from maps.distances import DistanceCalculator


class Load(Model):
    class LoadGroup(TextChoices):
        PP = 'PP', _('Priority pool')
        PPL = 'PPL', _('Priority pool loaded')
        URGENT = 'URGENT', _('Urgent')

    class LoadStatus(TextChoices):
        AVAILABLE = 'Available', _('Available')
        IN_PPROGRESS = 'In progress', _('In progress')
        COMPLETED = 'Completed', _('Completed')
        INVOICED = 'Invoiced', _('Invoiced')

    id = BigAutoField(primary_key=True)
    order_number = CharField(max_length=50)
    rate = PositiveSmallIntegerField()
    coordinator = ForeignKey(Profile, on_delete=RESTRICT, validators=[validate_coordinator], null=True, blank=True,
                             related_name='coordinator')
    entered_by = ForeignKey(Profile, on_delete=RESTRICT, related_name='entered_by')
    driver = ForeignKey(Driver, on_delete=RESTRICT, validators=[driver_for_load_validator], null=True, blank=True)
    trailer = ForeignKey(Trailer, on_delete=RESTRICT, null=True, blank=True)
    empty_miles = PositiveSmallIntegerField(null=True, blank=True)  # todo: define on save method
    loaded_miles = PositiveSmallIntegerField(null=True, blank=True)     # todo: define on save method
    group = CharField(max_length=6, choices=LoadGroup.choices)
    status = CharField(max_length=11, choices=LoadStatus.choices, default=LoadStatus.AVAILABLE)
    TONU = BooleanField(default=False) # add rule on save method
    notes = TextField(max_length=100, null=True, blank=True)
    broker_company = ForeignKey(BrokerCompany, on_delete=RESTRICT)

    @staticmethod
    def get_first_pu_stage(load):
        pu_stages = LoadUnloadStage.objects.filter(load=load.id).filter(type=True).order_by('order_number')
        if pu_stages:
            return pu_stages[0]
        return None

    @staticmethod
    def get_last_del_stage(load):
        del_stages = LoadUnloadStage.objects.filter(load=load.id).filter(type=False).order_by('-order_number')
        if del_stages:
            return del_stages[0]
        return None

    def get_empty_miles(self):
        if self.driver:
            last_unload_stage = Driver.get_last_unload_stage(self.driver)
            if last_unload_stage:
                last_location = last_unload_stage.facility.address
            else:
                last_location = CarrierCompany.objects.get(is_main=True).address
            print(last_location)
            print(Load.get_first_pu_stage(self).facility.address)
            DistanceCalculator.calculate([last_location, Load.get_first_pu_stage(self).facility.address])

    def get_loaded_miles(self):
        pass

    def set_TONU(self):
        pass


class Accessorial(Model):
    class AccessorialReason(TextChoices):
        DETENTION = 'DETENTION', _('Detention')
        LAYOVER = 'LAYOVER', _('Layover')
        EXTRA_MILES = 'EXTRA MILES', _('Extra miles')

    id = AutoField(primary_key=True)
    reason = CharField(max_length=11, choices=AccessorialReason.choices)
    amount = PositiveSmallIntegerField()
    load = ForeignKey(Load, on_delete=CASCADE)


class LoadUnloadStage(Model):
    id = BigAutoField(primary_key=True)
    type = BooleanField(default=True)
    load = ForeignKey(Load, on_delete=CASCADE)
    order_number = PositiveSmallIntegerField()
    time_from = DateTimeField()
    time_to = DateTimeField()
    actual_time_from = DateTimeField(null=True, blank=True)
    actual_time_to = DateTimeField(null=True, blank=True)
    facility = ForeignKey(Facility, on_delete=RESTRICT)
    note = TextField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = [['load', 'order_number', 'type'],]

    def __str__(self):
        return 'Order# {}|Stage# {}|Facility: {}'.format(self.load.order_number, self.order_number, self.facility)