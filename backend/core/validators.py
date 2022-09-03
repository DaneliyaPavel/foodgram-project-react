import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

SLUG_REGEX = '[-a-zA-Z0-9_]+$'


def slug_validation(value):
    slug_re = re.compile(SLUG_REGEX)

    if not slug_re.match(value):
        raise ValidationError(
            _('Slugs must consist of letters, numbers, '
              'underscores or hyphens.'),
            params={'value': value},
        )
