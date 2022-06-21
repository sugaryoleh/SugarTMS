from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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