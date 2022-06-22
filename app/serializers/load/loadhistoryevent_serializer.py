from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.load.loadhistoryevent import LoadHistoryEvent


class LoadHistoryEventSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = LoadHistoryEvent
        fields = '__all__'
