import mimetypes
import os

from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.load.load import Load
from app.models.load.loadfile import LoadFile
from app.serializers.load.loadfile_serializer import LoadFileSerializer


def download_load_file_view(request, pk):
    BASE_DIR = '/home/sugaryoleh/py/SugarTMS/filesss'
    # Define text file name
    file = LoadFile.objects.get(pk=pk)
    filename = file.file.name
    # Define the full file path
    filepath = '{}/{}'.format(BASE_DIR, filename)
    print(filepath)
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


@permission_classes([IsAuthenticated])
class LoadInvoiceView(APIView):
    def get(self, request, load):
        to_be_invoiced = Load.objects.get(pk=load)
        to_be_invoiced.invoice()
        return HttpResponse('to_be_invoiced')


@permission_classes([IsAuthenticated])
class LoadFilesView(APIView):
    model = LoadFile
    serializer = LoadFileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = (FileUploadParser,)
    template_name = 'load/load_files.html'

    def get(self, request, load):
        serializer = self.serializer(context={'request': request})

        files = LoadFile.objects.filter(load=load)
        for file in files:
            print(type(file.__dict__['file']))
        return Response({'serializer': serializer,
                         'title': self.model._meta.verbose_name.title(),
                         'load': load,
                         'pk': load,
                         'files': files,
                         })

    def post(self, request, load):
        print('IT\'S ALIVE')
        return HttpResponse('good')
        # serializer = self.serializer(data=request.data, context={'request': request})
        # if not serializer.is_valid():
        #     return Response({'title': self.model._meta.verbose_name.title(),
        #                      'serializer': serializer,
        #                      'load': load,
        #                      })
        # serializer.save()
        # return redirect('{}-list'.format(self.model._meta.verbose_name_raw.replace(' ', '')))
