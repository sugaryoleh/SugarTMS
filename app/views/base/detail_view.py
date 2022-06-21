from django.shortcuts import redirect
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


@permission_classes([IsAuthenticated])
class DetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detail.html'
    serializer = None
    model = None

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(obj, context={'request': request})
        return Response({'serializer': serializer,
                         'title': self.model._meta.verbose_name.title(),
                         'pk': pk,
                         'view_name': '{}-detail'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                         'delete_view_name': '{}-delete'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                         })

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(obj, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer,
                             'title': self.model._meta.verbose_name.title(),
                             'pk': pk,
                             'view_name': '{}-detail'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                             'delete_view_name': '{}-delete'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                             })
        serializer.save()
        return redirect('{}-list'.format(self.model._meta.verbose_name_raw.replace(' ', '')))
