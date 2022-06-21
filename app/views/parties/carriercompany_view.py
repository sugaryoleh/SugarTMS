from app.models.parties.carriercompany import CarrierCompany
from app.serializers.parties.carriercompany_serializer import CarrierCompanySerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class CarrierCompanyAdd(AddView):
    serializer = CarrierCompanySerializer
    model = CarrierCompany


class CarrierCompanyDetail(DetailView):
    serializer = CarrierCompanySerializer
    model = CarrierCompany


class CarrierCompanyDelete(DeleteView):
    serializer = CarrierCompanySerializer
    model = CarrierCompany


class CarrierCompanyList(ListView):
    serializer = CarrierCompanySerializer
    model = CarrierCompany
