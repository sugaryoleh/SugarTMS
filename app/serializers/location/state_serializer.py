from rest_framework.serializers import HyperlinkedModelSerializer

from app.models.location.state import State


class StateSerializer(HyperlinkedModelSerializer):
    url_fields = []

    class Meta:
        model = State
        fields = '__all__'
