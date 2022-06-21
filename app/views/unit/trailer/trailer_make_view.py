from app.models.unit.trailer import TrailerMake
from app.serializers.unit.trailer_serializer import TrailerMakeSerializer
from app.views.base.add_view import AddView
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView
from app.views.base.list_view import ListView


class TrailerMakeAdd(AddView):
    serializer = TrailerMakeSerializer
    model = TrailerMake


class TrailerMakeDetail(DetailView):
    serializer = TrailerMakeSerializer
    model = TrailerMake


class TrailerMakeDelete(DeleteView):
    serializer = TrailerMakeSerializer
    model = TrailerMake


class TrailerMakeList(ListView):
    serializer = TrailerMakeSerializer
    model = TrailerMake
