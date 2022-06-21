from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.parties.carriercompany import CarrierCompany


class CarrierCompanySerializer(HyperlinkedModelSerializer):
    url_fields = ['address']

    class Meta:
        model = CarrierCompany
        fields = '__all__'
