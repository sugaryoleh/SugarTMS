from app.models.unit.trailer import Trailer
from app.serializers.unit.trailer_serializer import TrailerSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TrailerAdd(AddView):
    serializer = TrailerSerializer
    model = Trailer


class TrailerDetail(DetailView):
    serializer = TrailerSerializer
    model = Trailer


class TrailerDelete(DeleteView):
    serializer = TrailerSerializer
    model = Trailer


class TrailerList(ListView):
    serializer = TrailerSerializer
    model = Trailer
