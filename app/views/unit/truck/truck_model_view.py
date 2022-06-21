from app.models.unit.truck import TruckModel
from app.serializers.unit.truck_serializer import TruckModelSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TruckModelAdd(AddView):
    serializer = TruckModelSerializer
    model = TruckModel


class TruckModelDetail(DetailView):
    serializer = TruckModelSerializer
    model = TruckModel


class TruckModelDelete(DeleteView):
    serializer = TruckModelSerializer
    model = TruckModel


class TruckModelList(ListView):
    serializer = TruckModelSerializer
    model = TruckModel
