from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.parties.brokercompany import BrokerCompany


class BrokerCompanySerializer(HyperlinkedModelSerializer):
    url_fields = ['address']

    class Meta:
        model = BrokerCompany
        fields = '__all__'
