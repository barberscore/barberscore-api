import floppyforms as forms
from apps.noncense.models import MobileUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = MobileUser
        fields = ('first_name', 'last_name', 'prediction')
