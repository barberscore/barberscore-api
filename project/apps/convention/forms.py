from haystack.forms import SearchForm

from django import forms


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
