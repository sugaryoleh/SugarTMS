from django.db.models import Model, AutoField, CharField, PositiveSmallIntegerField, ForeignKey, CASCADE, RESTRICT, \
    TextField, ManyToManyField, OneToOneField

from app.models.validators import validate_VIN, validate_unit_year


class Unit:
    id = AutoField(primary_key=True)
    name = CharField(max_length=10, unique=True)
    year = PositiveSmallIntegerField(validators=[validate_unit_year])
    note = TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class UnitMake(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=20, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class UnitModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=20, unique=True)

    def __str__(self):
        return '{} {}'.format(self.make.name, self.name)


class TrailerMake(UnitMake):
    pass


class TrailerModel(UnitModel):
    make = ForeignKey(TrailerMake, on_delete=CASCADE)


class Trailer(Model, Unit):
    model = ForeignKey(TrailerModel, on_delete=RESTRICT)


class TruckMake(UnitMake):
    pass


class TruckModel(UnitModel):
    make = ForeignKey(TruckMake, on_delete=CASCADE)


class Truck(Model, Unit):
    model = ForeignKey(TruckModel, on_delete=RESTRICT)
    vin = CharField(max_length=10, validators=[validate_VIN])


class UnitGroup(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=20)
    description = TextField(max_length=100)


class TruckGroup(UnitGroup):
    trucks = ManyToManyField(Truck)


class TrailerGroup(UnitGroup):
    trailers = ManyToManyField(Trailer)