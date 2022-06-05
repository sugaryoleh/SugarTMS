from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_driver_license(value):
    driver_license_number_length = 10
    if not value.isdigit():
        raise ValidationError(_('"Driver license" value must contain digits only'))
    if len(value) != driver_license_number_length:
        raise ValidationError(_('"Driver license" value length must be equal {}'.format(driver_license_number_length)))


def validate_coordinator(value):
    from app.models.users.profile import Profile
    if not Profile.objects.get(pk=value.id).is_coordinator:
        raise ValidationError(_('User is not coordinator'))