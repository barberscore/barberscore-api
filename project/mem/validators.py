from django.core.exceptions import ValidationError
from datetime import date

def validate_bhs_id(value):
    if not 100000 < value < 999999:  # Your conditions here
        raise ValidationError(
            "Must be between 100000 and 999999"
        )

def validate_birth_date(value):
    if not date(1900, 1, 1) < value < date(2015, 1, 1):  # Your conditions here
        raise ValidationError(
            "The birthdate must be reasonable."
        )
