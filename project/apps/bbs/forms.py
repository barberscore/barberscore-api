from django import forms

from noncense.models import (
    MobileUser,
)

from .models import (
    Rating,
)


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['user', 'performance']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MobileUser
        fields = ('first_name', 'last_name',)
