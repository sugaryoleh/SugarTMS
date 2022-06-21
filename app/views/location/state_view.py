from app.models.location.state import State
from app.serializers.location.state_serializer import StateSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


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
    serializer = StateSerializer
    model = State
