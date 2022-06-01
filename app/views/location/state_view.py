from django.shortcuts import redirect
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.location.state import State
from app.serializers.location.state_serializer import StateSerializer


class StateAdd(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'state_add.html'

    def get(self, request):
        serializer = StateSerializer()
        return Response({'serializer': serializer})

    def post(self, request):

        serializer = StateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'state': serializer.data})
        serializer.save()
        return redirect('state-list')


class StateList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'state_list.html'

    def get(self, request):
        queryset = State.objects.all()
        return Response({'states': queryset})


class StateDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'state_detail.html'

    def get(self, request, pk):
        state = get_object_or_404(State, pk=pk)
        serializer = StateSerializer(state)
        return Response({'serializer': serializer, 'state': state})

    def post(self, request, pk):
        state = get_object_or_404(State, pk=pk)
        serializer = StateSerializer(state, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'state': state})
        serializer.save()
        return redirect('state-list')


class StateDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'state_delete.html'

    def get(self, request, pk):
        state = get_object_or_404(State, pk=pk)
        return Response({'state': state})

    def post(self, request, pk):
        state = get_object_or_404(State, pk=pk)
        state.delete()
        return redirect('state-list')
