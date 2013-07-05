import floppyforms as forms
from floppyforms.widgets import PhoneNumberInput


class AuthRequestForm(forms.Form):
    mobile = forms.CharField(widget=PhoneNumberInput())


class AuthResponseForm(forms.Form):
    code = forms.CharField(widget=PhoneNumberInput())


class AltLoginForm(forms.Form):
    mobile = forms.CharField(widget=PhoneNumberInput())
