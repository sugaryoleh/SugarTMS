from django.test import TestCase

from app.models.driver.driver import Driver
from app.models.load.load import Load
from app.models.parties.brokercompany import BrokerCompany
from app.models.parties.logisticscompany import LogisticsCompany
from app.models.users.profile import Profile


class LoadCreateTestCase(TestCase):

    @staticmethod
    def get_coordinator():
        return Profile.objects.filter(is_coordinator=True)

    @staticmethod
    def get_driver():
        return Driver.objects.first()

    @staticmethod
    def get_logistics_company():
        return LogisticsCompany.objects.first()

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
        'notes': None,
        'broker_company': BrokerCompany,
        'dispatched': False
    }

    def setUp(self):
        Load.objects.create(order_number=self.input_data['order_number'], rate=self.input_data['rate'],
                            total=self.input_data['total'],  coordinator=self.input_data['coordinator'],
                            entered_by=self.input_data['entered_by'], driver=self.input_data['driver'],
                            trailer=self.input_data['trailer'], group=self.input_data['group'],
                            status=self.input_data['status'], notes=self.input_data['notes'],
                            broker_company=self.input_data['broker_company'],
                            dispatched=self.input_data['dispatched'])

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
        self.assertEqual(load.logistics_company, self.input_data['logistics_company'])
        self.assertEqual(load.dispatched, self.input_data['dispatched'])

