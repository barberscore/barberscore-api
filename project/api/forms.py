import uuid

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
        pk = uuid.uuid4()
        user.username = "orphan|{0}".format(str(pk))
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.bhs_id = self.cleaned_data['bhs_id']
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
