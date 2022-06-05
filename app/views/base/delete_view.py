from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


@permission_classes([IsAuthenticated])
class DeleteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'delete.html'
    serializer = None
    model = None

    @login_required
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return Response({'obj': obj,
                         'view_name': '{}-delete'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                         })

    @login_required
    def post(self, request, pk):
        state = get_object_or_404(self.model, pk=pk)
        state.delete()
        return redirect('{}-list'.format(self.model._meta.verbose_name_raw.replace(' ', '')))
