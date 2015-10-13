from django.core.exceptions import ValidationError


def validate_trimmed(value):
    if value.endswith(" ") or value.startswith(" "):
        raise ValidationError(
            'Value must not start or end with white space.',
            code='invalid',
        )
