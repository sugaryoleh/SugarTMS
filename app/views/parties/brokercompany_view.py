from app.models.parties.brokercompany import BrokerCompany
from app.serializers.parties.brokercompany_serializer import BrokerCompanySerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class BrokerCompanyAdd(AddView):
    serializer = BrokerCompanySerializer
    model = BrokerCompany


class BrokerCompanyDetail(DetailView):
    serializer = BrokerCompanySerializer
    model = BrokerCompany


class BrokerCompanyDelete(DeleteView):
    serializer = BrokerCompanySerializer
    model = BrokerCompany


class BrokerCompanyList(ListView):
    serializer = BrokerCompanySerializer
    model = BrokerCompany
