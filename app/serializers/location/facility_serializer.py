from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.location.facility import Facility


class FacilitySerializer(HyperlinkedModelSerializer):
    url_fields = ['address']

    class Meta:
        model = Facility
        fields = '__all__'
