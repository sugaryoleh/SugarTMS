from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.driver.driver import Driver
from app.models.driver.driverfile import DriverFile
from app.models.driver.ticket import Ticket


class DriverSerializer(HyperlinkedModelSerializer):
    url_fields = ['truck', 'company', 'coordinator', 'license_state']

    class Meta:
        model = Driver
        fields = '__all__'


class DriverFileSerializer(HyperlinkedModelSerializer):
    url_fields = ['added_by', 'driver']

    class Meta:
        model = DriverFile
        fields = '__all__'


class TicketSerializer(HyperlinkedModelSerializer):
    url_fields = ['added_by', 'driver', 'issue_state']

    class Meta:
        model = Ticket
        fields = '__all__'
