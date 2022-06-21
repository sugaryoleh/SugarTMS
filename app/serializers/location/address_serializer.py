from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.location.address import Address


class AddressSerializer(HyperlinkedModelSerializer):
    url_fields = ['state']

    class Meta:
        model = Address
        fields = '__all__'
