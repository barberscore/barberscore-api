import floppyforms as forms
from floppyforms.widgets import PhoneNumberInput


class LoginForm(forms.Form):
    mobile = forms.CharField(widget=PhoneNumberInput())
