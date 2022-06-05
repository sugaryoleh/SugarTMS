from django.core.files import File
from django.db.models import Model, BigAutoField, BooleanField, ForeignKey, PositiveSmallIntegerField, \
    RESTRICT, TextField, CharField, TextChoices, QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from app.models.driver.driver import Driver
from app.models.driver.validators import validate_coordinator
from app.models.load.validators import driver_for_load_validator
from app.models.parties.brokercompany import BrokerCompany
from app.models.parties.carriercompany import CarrierCompany
from app.models.unit.trailer import Trailer
from app.models.users.profile import Profile
from file_generator.invoices import generate_invoice
from maps.distances import DistanceCalculator
from msg.messages import send_message


class Load(Model):
    class LoadGroup(TextChoices):
        PP = 'PP', _('Priority pool')
        PPL = 'PPL', _('Priority pool loaded')
        URGENT = 'URGENT', _('Urgent')

    class LoadStatus(TextChoices):
        SET_UP = 'Set up', _('Set up')
        AVAILABLE = 'Available', _('Available')
        PENDING = 'Pending', _('Pending')
        IN_PPROGRESS = 'In progress', _('In progress')
        COMPLETED = 'Completed', _('Completed')
        INVOICED = 'Invoiced', _('Invoiced')

    id = BigAutoField(primary_key=True)
    order_number = CharField(max_length=50)
    rate = PositiveSmallIntegerField()
    total = PositiveSmallIntegerField(null=True, blank=True)
    coordinator = ForeignKey(Profile, on_delete=RESTRICT, validators=[validate_coordinator], null=True, blank=True,
                             related_name='coordinator')
    entered_by = ForeignKey(Profile, on_delete=RESTRICT, related_name='entered_by')
    driver = ForeignKey(Driver, on_delete=RESTRICT, validators=[driver_for_load_validator], null=True, blank=True)
    trailer = ForeignKey(Trailer, on_delete=RESTRICT, null=True, blank=True)
    group = CharField(max_length=6, choices=LoadGroup.choices)
    status = CharField(max_length=11, choices=LoadStatus.choices)
    notes = TextField(max_length=100, null=True, blank=True)
    broker_company = ForeignKey(BrokerCompany, on_delete=RESTRICT)
    dispatched = BooleanField(default=False)
    invoice_generated = BooleanField(default=False, editable=False)

    def just_created(self):
        return not Load.objects.filter(pk=self.pk).exists()

    def load_status_changed(self):
        before = Load.objects.get(pk=self.id)
        return before.status != self.status

    def save(self, *args, **kwargs):
        if self.just_created():
            self.status = self.LoadStatus.SET_UP
            self.total = self.rate
        else:
            if self.load_status_changed():
                from app.models.load.loadhistoryevent import LoadHistoryEvents
                LoadHistoryEvents.status_changed(self)
        if not Load.LoadManager.perform_checks(self):
            raise Exception("Inappropriate status {} for the load".format(self.status))

        super(Load, self).save(*args, **kwargs)

    def __str__(self):
        first_pu = self.LoadManager.get_first_pu_stage(self)
        last_del = self.LoadManager.get_last_del_stage(self)
        if first_pu:
            first_pu = '{}, {}'.format(first_pu.facility.address.city, first_pu.facility.address.state.code)
        if last_del:
            last_del = '{}, {}'.format(last_del.facility.address.city, last_del.facility.address.state.code)
        return 'Order#{} | {} -> {}'.format(self.order_number, first_pu, last_del)

    def get_accessorial_total(self):
        acum = 0
        from app.models.load.accessorial import Accessorial
        for accessorial in Accessorial.objects.filter(load=self.id):
            acum += accessorial.amount
        return acum

    def invoice(self):
        carrier = CarrierCompany.objects.get(is_main=True)
        file_name = generate_invoice(self, carrier)
        from app.models.load.loadfile import LoadFile
        LoadFile(type=LoadFile.FileType.INVOICE, load=self, file=File(open(file_name))).save()

    class LoadManager:
        @staticmethod
        def dispatch(driver, load):
            msg = 'PU: {pu_time}\nCompany: {pu_company}\nAddress: {pu_address}\n\nDEL: {del_time}\n' \
                  'Company: {del_company}\nAddress: {del_address}\nLoad# {load_number}'
            pu = load.LoadManager.get_first_pu_stage()
            pu_time = '{} - {}'.format(pu.time_from, pu.time_to)
            pu_company = pu.facility.name
            pu_address = pu.facility.address
            _del = load.LoadManager.get_last_del_stage()
            del_time = '{} - {}'.format(_del.time_from, _del.time_to)
            del_company = _del.facility.name
            del_address = _del.facility.add
            send_message(msg.format(pu_time=pu_time, pu_company=pu_company, pu_address=pu_address, del_time=del_time,
                                    del_company=del_company, del_address=del_address))

        @staticmethod
        def clean_load_stages(load):
            from app.models.load.loadstage import LoadStage
            stages = LoadStage.objects.filter(load=load.id)
            if stages.exists():
                for stage in stages:
                    LoadStage.LoadStageManager.clean_stage(stage)

        @staticmethod
        def get_first_pu_stage(load):
            from app.models.load.loadstage import LoadStage
            pu_stage = LoadStage.objects.filter(load=load.id).filter(type=True).filter(order_number=1)
            if pu_stage.exists():
                return pu_stage[0]
            return None

        @staticmethod
        def get_load_stages(load, type=True):
            from app.models.load.loadstage import LoadStage
            load_stages = LoadStage.objects.filter(load=load.id).filter(type=type).order_by('order_number')
            if load_stages.exists():
                return load_stages
            return None

        @staticmethod
        def get_last_del_stage(load):
            from app.models.load.loadstage import LoadStage
            del_stages = LoadStage.objects.filter(load=load.id).filter(type=False).order_by('-order_number')
            if del_stages.exists():
                return del_stages[0]
            return None

        @staticmethod
        def get_previous_load(load):
            lds = load.LoadManager.get_last_del_stage(load)
            from app.models.load.loadstage import LoadStage
            previous_unloads = LoadStage.objects.filter(type=False).filter(time_to__lt=lds.time_to).order_by('-time_to')
            if previous_unloads.exists():
                previous_unload_stage = previous_unloads[0]
                return Load.objects.get(id=previous_unload_stage.load.id)
            return None

        @staticmethod
        def get_empty_miles(load):
            if load.driver:
                last_location = CarrierCompany.objects.get(is_main=True).address
                previous_load = Load.get_previous_load(load)
                if previous_load:
                    ll = load.LoadManager.get_last_del_stage(previous_load).facility.address
                    if ll:
                        last_location = ll
                first_pickup = Load.LoadManager.get_first_pu_stage(load).facility.address
                distance = DistanceCalculator.calculate([last_location, first_pickup])
                return round(distance)
            else:
                return None

        @staticmethod
        def get_loaded_miles(load):
            load_stages = Load.LoadManager.get_load_stages(load, type=True)
            unload_stages = Load.LoadManager.get_load_stages(load, type=False)
            if load_stages and unload_stages:
                load_addresses = list(load.facility.address for load in load_stages)
                unload_addresses = list(load.facility.address for load in unload_stages)
                distance = DistanceCalculator.calculate(load_addresses + unload_addresses)
                return round(distance)
            return None

        @staticmethod
        def check_set_up(load):
            from app.models.load.loadstage import LoadStage
            stages = LoadStage.objects.filter(load=load.id)
            return stages.filter(type=True).exists() and stages.filter(type=False).exists() and Load.LoadManager.check_order(stages)

        @staticmethod
        def check_available(load):
            if load.driver is None:
                return True
            return False

        @staticmethod
        def check_pending(load):
            if load.driver is None:
                return False
            return True

        @staticmethod
        def check_in_progress(load):
            if load.trailer is not None:
                if load.dispatched:
                    last_load = Load.LoadManager.get_previous_load(load)
                    if last_load is None or (last_load.status == load.LoadStatus.COMPLETED or
                                             last_load.status == load.LoadStatus.INVOICED):
                        return True
            return False

        @staticmethod
        def check_completed(load):
            load_stages = Load.LoadManager.get_load_stages(load, True)
            unload_stages = Load.LoadManager.get_load_stages(load, False)
            all_stages = list(load_stages) + list(unload_stages)
            for stage in all_stages:
                if stage.actual_time_from is None or stage.actual_time_to is None:
                    return False
            return True

        @staticmethod
        def check_invoiced(load):
            return load.invoice_generated

        @staticmethod
        def perform_checks(load):
            checks = {
                Load.LoadStatus.SET_UP: [],
                Load.LoadStatus.AVAILABLE: [Load.LoadManager.check_set_up, Load.LoadManager.check_available],
                Load.LoadStatus.PENDING: [Load.LoadManager.check_set_up, Load.LoadManager.check_pending],
                Load.LoadStatus.IN_PPROGRESS: [Load.LoadManager.check_set_up, Load.LoadManager.check_pending,
                                               Load.LoadManager.check_in_progress],
                Load.LoadStatus.COMPLETED: [Load.LoadManager.check_set_up, Load.LoadManager.check_pending,
                                            Load.LoadManager.check_in_progress, Load.LoadManager.check_completed],
                Load.LoadStatus.INVOICED: [Load.LoadManager.check_set_up, Load.LoadManager.check_pending,
                                           Load.LoadManager.check_in_progress, Load.LoadManager.check_completed,
                                           Load.LoadManager.check_invoiced],
            }
            return all(check(load) for check in checks[load.status])

        @staticmethod
        def check_order(stages: QuerySet) -> bool:
            pu_stages = stages.filter(type=True).order_by('order_number')
            del_stages = stages.filter(type=False).order_by('order_number')
            for i in range(len(pu_stages)):
                if pu_stages[i].order_number != i+1:
                    return False
            for i in range(len(del_stages)):
                if del_stages[i].order_number != i+1:
                    return False
            return True
                
        @staticmethod
        def normalize_order(stages):
            constant = 32767
            stages = stages.filter.order_by('order_number')
            for i in range(len(stages)):
                stages[i].order_number = constant - i
            for stage in stages:
                stage.save()
            for i in range(len(stages)):
                stages[i].order_number = i
            for stage in stages:
                stage.save()


@receiver(post_save, sender=Load)
def load_created(sender, instance, created, **kwargs):
    if created:
        from app.models.load.loadhistoryevent import LoadHistoryEvents
        LoadHistoryEvents.load_created(instance)
        if instance.driver is not None:
            LoadHistoryEvents.driver_assigned(instance)
