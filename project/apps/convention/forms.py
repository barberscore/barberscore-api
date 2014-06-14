from haystack.forms import SearchForm

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


class ContestantSearchForm(SearchForm):

    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(
            attrs={
                'class': 'input-lg form-control',
                'type': 'search',
                'autofocus': 'True'
            }
        ),
    )
