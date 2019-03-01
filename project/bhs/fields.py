from django.db.models import EmailField, CharField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class McEmailField(EmailField):
    def from_db_value(self, value, expression, connection):
        try:
            validate_email(value)
        except ValidationError:
            return ""
        return value.lower()


class McVoicePartField(CharField):
    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        return value.strip().lower()


class McGenderField(CharField):
    def from_db_value(self, value, expression, connection):
        gender_map = {
            'men': 'male',
            'women': 'female',
            'mixed': 'mixed',
        }
        try:
            return gender_map[value.lower()]
        except AttributeError:
            return None
