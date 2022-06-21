from app.models.driver.driver import Driver
from app.serializers.driver_serializer import DriverSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class DriverAdd(AddView):
    serializer = DriverSerializer
    model = Driver


class DriverDetail(DetailView):
    serializer = DriverSerializer
    model = Driver


class DriverDelete(DeleteView):
    serializer = DriverSerializer
    model = Driver


class DriverList(ListView):
    serializer = DriverSerializer
    model = Driver
