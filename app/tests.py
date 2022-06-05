import datetime
from unittest import TestCase

from django.core.exceptions import ValidationError

from app.models.driver.driver import Driver
from app.models.load.load import Load
from app.models.load.loadstage import LoadStage
from app.models.load.validators import driver_for_load_validator, validate_coordinator
from app.models.location.address import Address
from app.models.location.facility import Facility
from app.models.location.state import State
from app.models.parties.brokercompany import BrokerCompany
from app.models.parties.carriercompany import CarrierCompany
from app.models.unit.truck import Truck
from app.models.users.profile import Profile


class LoadValidatorsTest(TestCase):
    def test_driver_for_load_validator_truck_not_assigned(self):
        driver = Driver.objects.create(first_name='Test', last_name='Test', email='test@test.com', is_active=True,
                                       phone='+380562239356', home_address=Address.objects.first(),
                                       license_state=State.objects.first(), license_number='0912345658',
                                       hire_type=Driver.HireType.FLAT_RATE, coordinator=Profile.objects.first(),
                                       company=CarrierCompany.objects.first())
        with self.assertRaises(ValidationError):
            driver_for_load_validator(driver)
        driver.delete()

    def test_driver_for_load_validator_not_active(self):
        driver = Driver.objects.create(first_name='Test', last_name='Test', email='test1@test.com', is_active=False,
                                       phone='+380562229356', home_address=Address.objects.first(),
                                       license_state=State.objects.first(), license_number='0444345678',
                                       hire_type=Driver.HireType.FLAT_RATE, coordinator=Profile.objects.first(),
                                       company=CarrierCompany.objects.first(), truck=Truck.objects.first())
        with self.assertRaises(ValidationError):
            driver_for_load_validator(driver)
        driver.delete()

    def test_validate_coordinator(self):
        profile = Profile.objects.last()
        with self.assertRaises(ValidationError):
            validate_coordinator(profile)


class LoadTestCase(TestCase):

    @staticmethod
    def get_coordinator():
        return Profile.objects.filter(is_coordinator=True)[0]

    @staticmethod
    def get_driver():
        return Driver.objects.first()

    @staticmethod
    def get_broker_company():
        return BrokerCompany.objects.first()

    input_data = {
        'order_number': 'test',
        'rate': 1500,
        'total': 1500,
        'coordinator': get_coordinator(),
        'entered_by': get_coordinator(),
        'driver': get_driver(),
        'trailer': None,
        'group': Load.LoadGroup.PP,
        'status': Load.LoadStatus.SET_UP,
        'broker_company': get_broker_company(),
        'notes': None,
        'dispatched': False
    }

    def setUp(self):
        self.load = Load.objects.create(order_number=self.input_data['order_number'], rate=self.input_data['rate'],
                            total=self.input_data['total'],  coordinator=self.input_data['coordinator'],
                            entered_by=self.input_data['entered_by'], driver=self.input_data['driver'],
                            trailer=self.input_data['trailer'], group=self.input_data['group'],
                            status=self.input_data['status'], notes=self.input_data['notes'],
                            broker_company=self.input_data['broker_company'], dispatched=self.input_data['dispatched'])
        self.pu = LoadStage.objects.create(load=self.load, order_number=1, type=True, facility=Facility.objects.first(),
                                           time_from=datetime.datetime.now(), time_to=datetime.datetime.now())

        self._del = LoadStage.objects.create(load=self.load, order_number=1, type=False, facility=Facility.objects.last(),
                                             time_from=datetime.datetime.now(), time_to=datetime.datetime.now())
        self.address = Address.objects.create(country='USA', state=State.objects.get(code='NC'), city='Shelby',
                                         street='Walmart Dr', building=200, zip='28150')
        self.facility = Facility.objects.create(address=self.address, name='Walmart DC6070')


    def test_load_create(self):
        load = Load.objects.get(order_number=self.input_data['order_number'])
        self.assertEqual(load.order_number, self.input_data['order_number'])
        self.assertEqual(load.rate, self.input_data['rate'])
        self.assertEqual(load.total, self.input_data['total'])
        self.assertEqual(load.coordinator, self.input_data['coordinator'])
        self.assertEqual(load.entered_by, self.input_data['entered_by'])
        self.assertEqual(load.driver, self.input_data['driver'])
        self.assertEqual(load.trailer, self.input_data['trailer'])
        self.assertEqual(load.group, self.input_data['group'])
        self.assertEqual(load.status, self.input_data['status'])
        self.assertEqual(load.notes, self.input_data['notes'])
        self.assertEqual(load.broker_company, self.input_data['broker_company'])
        self.assertEqual(load.dispatched, self.input_data['dispatched'])

    def test_get_first_pu_stage(self):
        self.assertEqual(self.pu, Load.LoadManager.get_first_pu_stage(self.load))

    def test_get_last_del_stage(self):
        self.assertEqual(self._del, Load.LoadManager.get_last_del_stage(self.load))

    def test_rating(self):
        rating = 3.3
        self.assertEqual(self.facility.rating, rating)

    def __del__(self):
        self.facility.delete()
        self.address.delete()
        self.load.delete()
