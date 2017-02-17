from django import forms

from .models import User


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['person'].email
        user.set_password(None)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
