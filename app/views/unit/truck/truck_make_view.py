from app.models.unit.truck import TruckMake
from app.serializers.unit.truck_serializer import TruckMakeSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TruckMakeAdd(AddView):
    serializer = TruckMakeSerializer
    model = TruckMake


class TruckMakeDetail(DetailView):
    serializer = TruckMakeSerializer
    model = TruckMake


class TruckMakeDelete(DeleteView):
    serializer = TruckMakeSerializer
    model = TruckMake


class TruckMakeList(ListView):
    serializer = TruckMakeSerializer
    model = TruckMake
