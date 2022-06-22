from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.load.accessorial import Accessorial
from app.serializers.load.accessorial_serializer import AccessorialSerializer


@permission_classes([IsAuthenticated])
class AccessorialsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'load/accessorials.html'
    model = Accessorial
    serializer = AccessorialSerializer

    def get(self, request, load):
        accessorials = Accessorial.objects.filter(load=load)
        print(accessorials)
        return Response({
            'accessorials': accessorials,
            'pk': load,
        })
