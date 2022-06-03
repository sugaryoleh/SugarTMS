from django.shortcuts import redirect, get_object_or_404
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class AddView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'add.html'
    serializer = None
    model = None
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = self.serializer(context={'request': request})
        return Response({'title': self.model._meta.verbose_name.title(),
                         'view_name': '{}-add'.format(self.model._meta.verbose_name_raw),
                         'serializer': serializer,
                         'style': self.style,
                         })

    def post(self, request):
        serializer = self.serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'title': self.model._meta.verbose_name.title(),
                             'view_name': '{}-add'.format(self.model._meta.verbose_name_raw),
                             'serializer': serializer,
                             })
        serializer.save()
        return redirect('{}-list'.format(self.model._meta.verbose_name_raw))


class DetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detail.html'
    serializer = None
    model = None
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(obj, context={'request': request})
        return Response({'serializer': serializer,
                         'title': self.model._meta.verbose_name.title(),
                         'pk': obj.pk,
                         'view_name': '{}-detail'.format(self.model._meta.verbose_name_raw),
                         'delete_view_name': '{}-delete'.format(self.model._meta.verbose_name_raw),
                         'style': self.style,
                         'links': 'state-add'
                         })

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(obj, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer,
                             'title': self.model._meta.verbose_name.title(),
                             'pk': obj.pk,
                             'view_name': '{}-detail'.format(self.model._meta.verbose_name_raw),
                             'delete_view_name': '{}-delete'.format(self.model._meta.verbose_name_raw),
                             })
        serializer.save()
        return redirect('{}-list'.format(self.model._meta.verbose_name_raw))


class DeleteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'delete.html'
    serializer = None
    model = None

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return Response({'obj': obj,
                         'view_name': '{}-delete'.format(self.model._meta.verbose_name_raw),
                         })

    def post(self, request, pk):
        state = get_object_or_404(self.model, pk=pk)
        state.delete()
        return redirect('{}-list'.format(self.model._meta.verbose_name_raw))


class ListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list.html'
    model = None

    def get(self, request):
        queryset = self.model.objects.all()
        return Response({'objects': queryset,
                         'detail_view_name': '{}-detail'.format(self.model._meta.verbose_name_raw),
                         'title': self.model._meta.verbose_name_plural.title()
                         })
