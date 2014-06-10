from django import forms

from .models import (
    Contestant,
)


class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = (
            'name',
        )


class QuartetForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = (
            'name',
            'lead',
            'tenor',
            'baritone',
            'bass',
        )
