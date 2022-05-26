from django.db.models import Model, CharField, AutoField, ForeignKey, RESTRICT, PositiveSmallIntegerField

from app.models.validators import validate_zip_code


class State(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    code = CharField(max_length=3)

    class Meta:
        unique_together = ('name', 'code')

    def __str__(self):
        return '{}'.format(self.code)


class Address(Model):
    id = AutoField(primary_key=True)
    country = CharField(max_length=56)
    state = ForeignKey(State, on_delete=RESTRICT)
    city = CharField(max_length=35)
    zip = CharField(max_length=10, validators=[validate_zip_code])
    street = CharField(max_length=35)
    building = PositiveSmallIntegerField()

    class Meta:
        unique_together = ('country', 'state', 'city', 'zip', 'street', 'building')

    def __str__(self):
        return '{} {}, {}, {} {}, {}'.format(self.building, self.street, self.city, self.state.code, self.zip,
                                             self.country)
