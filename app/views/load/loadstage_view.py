from django.shortcuts import redirect
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.load.load import Load
from app.models.load.loadstage import LoadStage
from app.serializers.load.loadstage_serializer import LoadStageSerializer


@permission_classes([IsAuthenticated])
class LoadStageListAddView(APIView):
    model = LoadStage
    serializer = LoadStageSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'load/stages.html'

    def get(self, request, load):
        serializer = self.serializer(context={'request': request})
        load_object = Load.objects.get(pk=load)
        picks = Load.LoadManager.get_load_stages(load_object, True)
        dels = Load.LoadManager.get_load_stages(load_object, False)
        return Response({'serializer': serializer,
                         'title': self.model._meta.verbose_name.title(),
                         'load': load,
                         'pk': load,
                         'picks': picks,
                         'dels': dels,
                         })

    def post(self, request, load):
        serializer = self.serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            print(serializer.data)

            return Response({'title': self.model._meta.verbose_name.title(),
                             'load': load,
                             'pk': load,
                             'serializer': serializer,
                             })
        serializer.save()
        return redirect(request.path_info)

