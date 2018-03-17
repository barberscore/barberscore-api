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
        user.email = self.cleaned_data['person'].email.lower()
        if self.cleaned_data['bhs_id']:
            name = "{0} [{1}]".format(
                self.cleaned_data['name'],
                self.cleaned_data['bhs_id'],
            )
        else:
            name = self.cleaned_data['name']
        user.name = name
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
