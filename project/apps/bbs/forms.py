import floppyforms
from apps.noncense.models import MobileUser

class ProfileForm(floppyforms.ModelForm):
    class Meta:
        model = MobileUser
        fields = ('first_name', 'last_name', 'prediction', 'time_zone')
