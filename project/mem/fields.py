# Django
from django.db.models import EmailField

class LowerEmailField(EmailField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value
