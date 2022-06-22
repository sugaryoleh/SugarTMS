from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.load.loadfile import LoadFile


class LoadFileSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = LoadFile
        fields = '__all__'
