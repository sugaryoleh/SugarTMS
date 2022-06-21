from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.load.loadstage import LoadStage


class LoadStageSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = LoadStage
        fields = '__all__'
