from django import forms

from django.forms.models import (
    inlineformset_factory,
)

from apps.api.models import (
    Contest,
    Judge,
    Person,
)


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        # label=popover_html(
        #     'Email',
        #     'help-login-email',
        #     'Please enter the email you used when you originally registered for the site.'
        # ),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Email",
                'autofocus': 'autofocus',
            },
        ),
        error_messages={
            'required': 'Please enter your email address.',
        },
    )
    password = forms.CharField(
        required=True,
        # label=popover_html(
        #     'Password',
        #     'help-login-password',
        #     'Please enter the password you used at registration.  If you have forgotten your password please contact support.'
        # ),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Password",
            },
        ),
        error_messages={
            'required': 'Please enter your password.',
        },
    )


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = [
            # 'organization',
            # 'level',
            # 'kind',
            # 'goal',
            # 'year',
            'panel',
            'rounds',
        ]
        widgets = {
            # 'organization': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     },
            # ),
            # 'level': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     },
            # ),
            # 'kind': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     },
            # ),
            # 'goal': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     },
            # ),
            # 'year': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     },
            # ),
            'panel': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'rounds': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        contest = super(ContestForm, self).save(commit=False)
        contest.build_contest()
        if commit:
            contest.save()
        return contest


class ImpanelForm(forms.ModelForm):
    # person = forms.ModelChoiceField(
    #     queryset=Person.objects.filter(
    #         name__startswith='David',
    #     ),
    #     widget=forms.Select,
    # )

    class Meta:
        model = Judge
        fields = [
            'contest',
            'person',
            # 'status',
            'category',
            'slot',
            # 'organization',
        ]
        extra = 0
        widgets = {
            'person': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly',
                },
            ),
            'slot': forms.Select(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly',
                },
            ),
            'contest': forms.HiddenInput(
            ),
        }

