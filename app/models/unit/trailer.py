from django.db.models import ForeignKey, CASCADE, RESTRICT, ManyToManyField

from .unit import UnitMake, UnitModel, Unit, UnitGroup


class TrailerMake(UnitMake):
    pass


class TrailerModel(UnitModel):
    make = ForeignKey(TrailerMake, on_delete=CASCADE)


class Trailer(Unit):
    model = ForeignKey(TrailerModel, on_delete=RESTRICT)


class TrailerGroup(UnitGroup):
    trailers = ManyToManyField(Trailer)
