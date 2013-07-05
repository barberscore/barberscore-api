import floppyforms as forms
# from floppyforms.widgets import PhoneNumberInput


from .models import (
    UserProfile,
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'nickname', 'prediction')
