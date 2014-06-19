from django import forms

from .models import (
    Profile,
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'nickname',
            'timezone',
        )
        widgets = {
            'nickname': forms.TextInput(
                attrs={
                    'class': 'form-control input-lg',
                    'placeholder': 'name/nickname',
                }
            ),
            'timezone': forms.Select(
                attrs={
                    'class': 'form-control input-lg',
                }
            ),
        }
