from app.models.location.state import State
from app.serializers.location.state_serializer import StateSerializer
from app.views.base import AddView, DetailView, DeleteView, ListView


class StateAdd(AddView):
    serializer = StateSerializer
    model = State


class StateDetail(DetailView):
    serializer = StateSerializer
    model = State


class StateDelete(DeleteView):
    serializer = StateSerializer
    model = State


class StateList(ListView):
    model = State
