import logging
log = logging.getLogger(__name__)

from django import forms
from .models import(
    TwilioMessage
)

from django.contrib.auth import get_user_model

User = get_user_model()


class MobileForm(forms.Form):
    mobile = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'input-lg',
                'placeholder': 'mobile number',
                'type': 'tel',
                'autofocus': 'True',
                # 'size': 30,
            }
        ),
        required=True,
        error_messages={
            'required': "Please enter your mobile number.",
            'invalid': "Please enter a valid mobile number."
        },
    )


class CodeForm(forms.Form):
    code = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'input-lg',
                'placeholder': 'code',
                'type': 'tel',
                'autofocus': 'True'
            }
        ),
        required=True,
        error_messages={
            'required': "Please enter the code we sent you."
        },
    )


class InboundForm(forms.ModelForm):
    class Meta:
        model = TwilioMessage
        fields = ('body',)
