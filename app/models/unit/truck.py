from django.db.models import ForeignKey, CASCADE, RESTRICT, CharField, ManyToManyField

from app.models.unit.unit import UnitMake, UnitModel, Unit, UnitGroup
from app.models.unit.validators import validate_VIN


class TruckMake(UnitMake):
    pass


class TruckModel(UnitModel):
    make = ForeignKey(TruckMake, on_delete=CASCADE)


class Truck(Unit):
    model = ForeignKey(TruckModel, on_delete=RESTRICT)
    vin = CharField(max_length=17, validators=[validate_VIN])


class TruckGroup(UnitGroup):
    trucks = ManyToManyField(Truck)
