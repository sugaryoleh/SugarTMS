from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView



class AddView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'add.html'
    serializer = None
    model = None

    def get(self, request):
        serializer = self.serializer(context={'request': request})

        return Response({'serializer': serializer,
                         'title': self.model._meta.verbose_name.title(),
                         'view_name': '{}-add'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                         })

    def post(self, request):
        serializer = self.serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'title': self.model._meta.verbose_name.title(),
                             'view_name': '{}-add'.format(self.model._meta.verbose_name_raw.replace(' ', '')),
                             'serializer': serializer,

                             })
        serializer.save()
        return redirect('{}-list'.format(self.model._meta.verbose_name_raw.replace(' ', '')))