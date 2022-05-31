from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def driver_for_load_validator(value):
    from app.models.driver.driver import Driver
    if not Driver.objects.get(pk=value).is_active:
        raise ValidationError(_('Driver must be active to be assigned to the load'))
    if Driver.objects.get(pk=value).truck is None:
        raise ValidationError(_('Driver must have truck assigned assigned to the load'))