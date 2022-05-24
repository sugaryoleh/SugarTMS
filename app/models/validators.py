import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re

from app.models.profile import Profile


def validate_unit_year(value):
    current_year = datetime.datetime.now().year
    if value > current_year+1:
        raise ValidationError(_('Given "Year" value "{}" is inappropriate'.format(value)))


def validate_VIN(value):
    if not value.isdigit():
        raise ValidationError(_('VIN value must contain digits only'))
    if len(value) != 17:
        raise ValidationError(_('VIN value length must be equal 17'))


def validate_driver_license(value):
    driver_license_number_length = 10
    if not value.isdigit():
        raise ValidationError(_('"Driver license" value must contain digits only'))
    if len(value) != driver_license_number_length:
        raise ValidationError(_('"Driver license" value length must be equal {}'.format(driver_license_number_length)))


def validate_zip_code(value):
    if not re.match('^[0-9]{5}(?:-[0-9]{4})?$', value):
        raise ValidationError(_('"ZIP" length must be equal 5 or 10'))


def validate_coordinator(value):
    if not Profile.objects.get(pk=value).is_coordinator:
        raise ValidationError(_('User is not coordinator'))


def validate_MC_number(value):
    MC_number_len = 6
    if not value.isdigit():
        raise ValidationError(_('MC value must contain digits only'))
    if len(value) != MC_number_len:
        raise ValidationError(_('MC value length must be equal {}}'.format(MC_number_len)))


def validate_DOT_number(value):
    DOT_number_len = 7
    if not value.isdigit():
        raise ValidationError(_('MC value must contain digits only'))
    if len(value) != DOT_number_len:
        raise ValidationError(_('MC value length must be equal {}'.format(DOT_number_len)))


def validate_logistics_company_rate(value):
    rate_len = 1
    if not value.isalpha():
        raise ValidationError(_('MC value must contain digits only'))
    if len(value) != rate_len:
        raise ValidationError(_('MC value length must be equal {}'.format(rate_len)))
