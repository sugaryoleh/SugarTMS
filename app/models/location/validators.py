import re
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError


def validate_zip_code(value):
    if not re.match('^[0-9]{5}(?:-[0-9]{4})?$', value):
        raise ValidationError(_('"ZIP" length must be equal 5 or 10'))