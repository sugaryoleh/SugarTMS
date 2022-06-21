from django.db.models import ForeignKey, CASCADE

from app.models.file import File
from app.models.unit.trailer import Trailer


class TrailerFile(File):
    trailer = ForeignKey(Trailer, on_delete=CASCADE)
