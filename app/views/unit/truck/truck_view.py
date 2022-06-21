from app.models.unit.truck import Truck
from app.serializers.unit.truck_serializer import TruckSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TruckAdd(AddView):
    serializer = TruckSerializer
    model = Truck


class TruckDetail(DetailView):
    serializer = TruckSerializer
    model = Truck


class TruckDelete(DeleteView):
    serializer = TruckSerializer
    model = Truck


class TruckList(ListView):
    serializer = TruckSerializer
    model = Truck
