import floppyforms as forms
# from django_localflavor_us import forms
from floppyforms.widgets import PhoneNumberInput


class AuthRequestForm(forms.Form):
    mobile = forms.CharField(widget=PhoneNumberInput())


class AuthResponseForm(forms.Form):
    code = forms.CharField(widget=PhoneNumberInput())


class AltLoginForm(forms.Form):
    mobile = forms.CharField(widget=PhoneNumberInput())
