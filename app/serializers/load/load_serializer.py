from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.load.load import Load


class LoadSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Load
        fields = '__all__'
