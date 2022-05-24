from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Model, AutoField, CharField, ForeignKey, RESTRICT, BooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from app.models.address import Address
from app.models.validators import validate_MC_number, validate_DOT_number, validate_logistics_company_rate


class LogisticsCompany(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True)
    address = ForeignKey(Address, on_delete=RESTRICT)
    MC = CharField(max_length=6, validators=[validate_MC_number], unique=True)
    DOT = CharField(max_length=7, validators=[validate_DOT_number], unique=True)
    rate = CharField(max_length=1, validators=[validate_logistics_company_rate])

    def __str__(self):
        return '{}'.format(self.name)


class BrokerCompany(LogisticsCompany):
    pass


class CarrierCompany(LogisticsCompany):
    is_main = BooleanField(default=False)

    def save(self, *args, **kwargs):
        existing = None
        try:
            existing = CarrierCompany.objects.get(pk=self.id)
        except ObjectDoesNotExist:
            pass
        finally:
            if existing:
                if self.is_main != existing.is_main and True in [obj.is_main for obj in CarrierCompany.objects.all()]:
                    raise ValidationError(_('The db must have one main CarrierCompany which is set once.'))
            super(LogisticsCompany, self).save(args, kwargs)

# @receiver(post_save, sender=CarrierCompany)
# def save_carrier_company(sender, instance, **kwargs):
#     if instance.is_main:
#         mains = sender.objects.filter(is_main=True)
#         for company in mains:
#             if company != instance:
#                 company.is_main = False
#                 company.save()
