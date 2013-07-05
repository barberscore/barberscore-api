import floppyforms as forms
# from floppyforms.widgets import PhoneNumberInput


from .models import (
    Rating,
    # UserProfile,
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


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('first_name', 'last_name', 'nickname', 'timezone')
