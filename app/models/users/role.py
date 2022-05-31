from django.db.models import Model, TextChoices, AutoField, CharField
from django.utils.translation import gettext_lazy as _


class Role(Model):

    class Department(TextChoices):
        DRM = 'DRM', _('Driver relationship management')
        SAFETY = 'SAFETY', _('Safety')
        OPERATIONS = 'OPERATIONS', _('Operations')
        SHOP = 'SHOP', _('Shop')
        ACCOUNTING = 'ACCOUNTING', _('Accounting')

    id = AutoField(primary_key=True)
    name = CharField(max_length=20, unique=True)
    department = CharField(max_length=10, choices=Department.choices)

    def __str__(self):
        return '{}/{}'.format(self.name, self.department)