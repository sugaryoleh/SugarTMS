from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.unit.truck import TruckMake, TruckModel, Truck, TruckGroup


class TruckMakeSerializer(HyperlinkedModelSerializer):
    url_fields = []

    class Meta:
        model = TruckMake
        fields = '__all__'


class TruckModelSerializer(HyperlinkedModelSerializer):
    url_fields = ['truckmake']

    class Meta:
        model = TruckModel
        fields = '__all__'


class TruckSerializer(HyperlinkedModelSerializer):
    url_fields = ['truckmake']

    class Meta:
        model = Truck
        fields = '__all__'


class TruckGroupSerializer(HyperlinkedModelSerializer):
    url_fields = ['trucks']

    class Meta:
        model = TruckGroup
        fields = '__all__'

