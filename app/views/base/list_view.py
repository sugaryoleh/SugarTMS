from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


@permission_classes([IsAuthenticated])
class ListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list.html'
    model = None
    serializer = None

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer(context={'request': request})
        return Response({'objects': queryset,
                         'serializer': serializer,
                         'add_view_name': '{}-add'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                         'detail_view_name': '{}-detail'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                         'title': self.model._meta.verbose_name_plural.title(),
                         })
