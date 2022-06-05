from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def driver_for_load_validator(value):
    from app.models.driver.driver import Driver
    if not Driver.objects.get(pk=value.id).is_active:
        raise ValidationError(_('Driver must be active to be assigned to the load'))
    if Driver.objects.get(pk=value.id).truck is None:
        raise ValidationError(_('Driver must have truck assigned assigned to the load'))


def validate_coordinator(value):
    from app.models.users.profile import Profile
    if not Profile.objects.get(pk=value.id).is_coordinator:
        raise ValidationError(_('User is not coordinator'))