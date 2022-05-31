from django.db.models import Model, CharField, AutoField, ForeignKey, RESTRICT, PositiveSmallIntegerField

from .state import State
from .validators import validate_zip_code


class Address(Model):
    id = AutoField(primary_key=True)
    country = CharField(max_length=56)
    state = ForeignKey(State, on_delete=RESTRICT)
    city = CharField(max_length=35)
    zip = CharField(max_length=10, validators=[validate_zip_code])
    street = CharField(max_length=35)
    building = PositiveSmallIntegerField()

    class Meta:
        unique_together = [('country', 'state', 'city', 'zip', 'street', 'building')]
        verbose_name_plural = 'addresses'

    def __str__(self):
        return '{} {}, {}, {} {}, {}'.format(self.building, self.street, self.city, self.state.code, self.zip,
                                             self.country)
