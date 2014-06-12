import floppyforms as forms

from .models import (
    Rating,
    Prediction,
)


from apps.convention.models import (
    Contestant,
)

class PlaceholderInput(forms.TextInput):
    template_name = 'placeholder_input.html'


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        exclude = ['user', 'performance']
        widgets = {
            'song_one': forms.PhoneNumberInput(attrs={'placeholder': 'Enter Score, 0-100'}),
            'song_two': forms.PhoneNumberInput(attrs={'placeholder': 'Enter Score, 0-100'}),
        }


class PredictionForm(forms.ModelForm):

    class Meta:
        model = Prediction
        exclude = ['user']
