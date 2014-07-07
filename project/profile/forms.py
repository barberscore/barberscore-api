from django import forms

from .models import (
    Profile,
    Note,
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
                    'placeholder': 'Nickname (public)',
                }
            ),
            'timezone': forms.Select(
                attrs={
                    'class': 'form-control input-lg',
                }
            ),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        field = (
            'note',
            'profile',
            'contestant',
        )
        widgets = {
            'note': forms.Textarea(
                attrs={
                    'class': 'form-control input-lg',
                    'placeholder': "Enter your notes here.  These will be private and only visible by you.",
                }
            ),
            'profile': forms.HiddenInput(),
            'contestant': forms.HiddenInput(),
        }
