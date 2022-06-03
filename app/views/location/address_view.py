from app.models.location.address import Address
from app.serializers.location.address_serializer import AddressSerializer
from app.views.base import AddView, DetailView, DeleteView, ListView


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
    model = Address
