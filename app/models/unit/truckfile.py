from django.db.models import ForeignKey, CASCADE

from app.models.file import File
from app.models.unit.truck import Truck


class TruckFile(File):
    truck = ForeignKey(Truck, on_delete=CASCADE)
