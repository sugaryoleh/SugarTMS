from django.db.models import Model, AutoField, CharField, PositiveSmallIntegerField, TextField

from app.models.unit.validators import validate_unit_year


class Unit(Model):
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


class UnitGroup(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=20)
    description = TextField(max_length=100)
