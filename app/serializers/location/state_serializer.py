from rest_framework.serializers import ModelSerializer

from app.models.location.state import State


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
