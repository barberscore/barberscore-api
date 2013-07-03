import floppyforms as forms
from floppyforms.widgets import PhoneNumberInput

from apps.noncense.models import (
    MobileUser,
)

from .models import (
    Rating,
)


class PlaceholderInput(forms.TextInput):
    template_name = 'placeholder_input.html'


class RatingForm(forms.ModelForm):
    # song_one = forms.IntegerField(initial=50)

    class Meta:
        model = Rating
        exclude = ['user', 'performance']
        widgets = {
            'song_one': forms.PhoneNumberInput(attrs={'placeholder': 'Enter Score, 0-100'}),
            'song_two': forms.PhoneNumberInput(attrs={'placeholder': 'Enter Score, 0-100'}),
    }

# class RatingForm(forms.Form):
#     song_one = forms.IntegerField(initial=50, widget=PhoneNumberInput())
#     song_two = forms.IntegerField(initial=50, widget=PhoneNumberInput())

#     class Meta:
#         model = Rating
#         exclude = ['user', 'performance']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MobileUser
        fields = ('first_name', 'last_name',)
