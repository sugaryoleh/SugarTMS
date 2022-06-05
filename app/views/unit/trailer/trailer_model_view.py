from app.models.unit.trailer import TrailerModel
from app.serializers.unit.trailer_serializer import TrailerModelSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TrailerModelAdd(AddView):
    serializer = TrailerModelSerializer
    model = TrailerModel


class TrailerModelDetail(DetailView):
    serializer = TrailerModelSerializer
    model = TrailerModel


class TrailerModelDelete(DeleteView):
    serializer = TrailerModelSerializer
    model = TrailerModel


class TrailerModelList(ListView):
    serializer = TrailerModelSerializer
    model = TrailerModel
