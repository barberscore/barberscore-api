from haystack.forms import SearchForm

from django import forms


class ContestantSearchForm(SearchForm):
    """
    Overrides the base Haystack search form.
    """

    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(
            attrs={
                'class': 'input-lg form-control',
                'type': 'search',
                'autofocus': 'True',
                'size': 30,
            }
        ),
    )
