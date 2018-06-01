# Django
from django import forms

# Local
from .models import User


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        inlines = []

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
