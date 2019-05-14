from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from uuid import UUID
from datetime import date

def validate_bhs_id(value):
    if not 0 < value < 999999:  # Your conditions here
        raise ValidationError(
            "Must be between 0 and 999999"
        )

def validate_birth_date(value):
    if not date(1900, 1, 1) < value < date(2015, 1, 1):  # Your conditions here
        raise ValidationError(
            "The birthdate must be reasonable."
        )

validate_tin = RegexValidator(
    r'(9\d{2})([ \-]?)([7]\d|8[0-8])([ \-]?)(\d{4})',
    message="""
        Must be a Taxpayer Idenfication Number
        in the form `XX-XXXXXXXX`.
    """,
)

validate_nopunctuation = RegexValidator(
    r'/[\p{L}]/ui',
    message="""
        Must not use punctuation.
    """,
)

validate_url = URLValidator()

def validate_uuid(value):
    try:
        UUID(value, version=4)
    except ValueError as e:
        raise e
