from django.shortcuts import redirect
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.load.load import Load
from app.serializers.load.load_serializer import LoadSerializer
from app.views.base.add_view import AddView
from app.views.base.detail_view import DetailView


class LoadAddView(AddView):
    model = Load
    serializer = LoadSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'title': self.model._meta.verbose_name.title(),
                             'view_name': 'load-add',
                             'serializer': serializer,

                             })
        serializer.save()
        return redirect('load-detail')


class LoadDetailView(DetailView):
    model = Load
    serializer = LoadSerializer
    template_name = 'load/load_profile.html'


@permission_classes([IsAuthenticated])
class LoadListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'load/load_list.html'
    model = Load
    serializer = LoadSerializer

    def get(self, request):
        loads = Load.objects.all()
        hat = ['Order#', 'Pick up', 'Delivery', 'Driver', 'Trailer', 'Rate']

        data = [{'id': load.pk, 'order_number': load.order_number, 'first_pu': Load.LoadManager.get_first_pu_stage(load),
                 'last_del': Load.LoadManager.get_last_del_stage(load), 'driver': load.driver, 'trailer': load.trailer,
                 'rate': load.rate} for load in loads]
        return Response({'data': data,
                         'hat': hat,
                         'add_view_name': 'load-add',
                         'detail_view_name': 'load-detail',
                         'title': self.model._meta.verbose_name_plural.title(),
                         })
