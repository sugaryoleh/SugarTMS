from app.models.location.facility import Facility
from app.serializers.location.facility_serializer import FacilitySerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class FacilityAdd(AddView):
    serializer = FacilitySerializer
    model = Facility


class FacilityDetail(DetailView):
    serializer = FacilitySerializer
    model = Facility


class FacilityDelete(DeleteView):
    serializer = FacilitySerializer
    model = Facility


class FacilityList(ListView):
    serializer = FacilitySerializer
    model = Facility
