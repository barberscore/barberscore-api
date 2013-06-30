from django import forms

from noncense.models import (
    MobileUser,
)

from .models import (
    Score,
)


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        exclude = ['user', 'performance']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MobileUser
        fields = ('first_name', 'last_name',)
