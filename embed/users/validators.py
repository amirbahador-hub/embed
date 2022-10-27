import re

from django.utils.translation import gettext as _
from django.core.exceptions import (
    ValidationError,
)


def integer_validator(password):
    """
    Validate whether the password contains numberic.
    """

    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must contain numberic characters."),
                code='password_must_contain_numberic_characters',
            )

def alphabet_validator(password):
    """
    Validate whether the password containes alphanumeric.
    """

    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
            _("password must contain alphanumeric characters."),
            code='password_must_contain_alphanumeric_characters',
            )

def special_characters_validator(password):
    """
    Validate whether the password contain special characters.
    """

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
            _("Password must contain special characters."),
            code='password_must_contain_special_characters',
            )

