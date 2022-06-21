from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.unit.trailer import TrailerMake, TrailerModel, Trailer, TrailerGroup
from app.models.unit.trailerfile import TrailerFile


class TrailerMakeSerializer(HyperlinkedModelSerializer):
    url_fields = []

    class Meta:
        model = TrailerMake
        fields = '__all__'


class TrailerModelSerializer(HyperlinkedModelSerializer):
    url_fields = ['trailermake']

    class Meta:
        model = TrailerModel
        fields = '__all__'


class TrailerSerializer(HyperlinkedModelSerializer):
    url_fields = ['trailermake']

    class Meta:
        model = Trailer
        fields = '__all__'


class TrailerGroupSerializer(HyperlinkedModelSerializer):
    url_fields = ['trailers']

    class Meta:
        model = TrailerGroup
        fields = '__all__'


class TrailerFileSerializer(HyperlinkedModelSerializer):
    url_fields = ['added_by', 'trailer']

    class Meta:
        model = TrailerFile
        fields = '__all__'
