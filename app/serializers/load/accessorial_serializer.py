from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.load.accessorial import Accessorial


class AccessorialSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Accessorial
        fields = '__all__'
