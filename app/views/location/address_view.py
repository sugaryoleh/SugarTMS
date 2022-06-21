from app.models.location.address import Address
from app.serializers.location.address_serializer import AddressSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class AddressAdd(AddView):
    serializer = AddressSerializer
    model = Address


class AddressDetail(DetailView):
    serializer = AddressSerializer
    model = Address


class AddressDelete(DeleteView):
    serializer = AddressSerializer
    model = Address


class AddressList(ListView):
    serializer = AddressSerializer
    model = Address
