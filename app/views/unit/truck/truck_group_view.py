from app.models.unit.truck import TruckGroup
from app.serializers.unit.truck_serializer import TruckGroupSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TruckGroupAdd(AddView):
    serializer = TruckGroupSerializer
    model = TruckGroup


class TruckGroupDetail(DetailView):
    serializer = TruckGroupSerializer
    model = TruckGroup


class TruckGroupDelete(DeleteView):
    serializer = TruckGroupSerializer
    model = TruckGroup


class TruckGroupList(ListView):
    serializer = TruckGroupSerializer
    model = TruckGroup
