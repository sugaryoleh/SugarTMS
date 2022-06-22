from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.load.loadhistoryevent import LoadHistoryEvent
from app.serializers.load.loadhistoryevent_serializer import LoadHistoryEventSerializer


@permission_classes([IsAuthenticated])
class LoadHistoryView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'load/load_history.html'
    model = LoadHistoryEvent
    serializer = LoadHistoryEventSerializer

    def get(self, request, load):
        events = LoadHistoryEvent.objects.filter(load=load)

        return Response({
            'events': events,
            'pk': load,
        })
