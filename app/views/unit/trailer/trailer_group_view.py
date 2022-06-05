from app.models.unit.trailer import TrailerGroup
from app.serializers.unit.trailer_serializer import TrailerGroupSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TrailerGroupAdd(AddView):
    serializer = TrailerGroupSerializer
    model = TrailerGroup


class TrailerGroupDetail(DetailView):
    serializer = TrailerGroupSerializer
    model = TrailerGroup


class TrailerGroupDelete(DeleteView):
    serializer = TrailerGroupSerializer
    model = TrailerGroup


class TrailerGroupList(ListView):
    serializer = TrailerGroupSerializer
    model = TrailerGroup
