from django.db.models import Model, AutoField, CharField, ForeignKey, RESTRICT, TextField, EmailField, FloatField
from phonenumber_field.modelfields import PhoneNumberField
from requests import HTTPError

from .address import Address


class Facility(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    address = ForeignKey(Address, on_delete=RESTRICT)
    note = TextField(max_length=100, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = EmailField(null=True, blank=True)
    rating = FloatField(null=True, blank=True)

    class Meta:
        unique_together = [('name', 'address')]
        verbose_name_plural = 'facilities'

    def save(self, *args, **kwargs):
        from maps.places import PlaceResolver
        missing_fields = ['rating']
        try:
            pr = PlaceResolver(self)
            details = pr.get_place_details(*missing_fields)
            for detail in details:
                self.__setattr__(detail, details[detail])
        except HTTPError as error:
            print(error)
        super(Facility, self).save(*args, **kwargs)

    def __str__(self):
        return '{}/ {},{}'.format(self.name, self.address.city, self.address.state.code)