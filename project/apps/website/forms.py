from django import forms

from django.forms import (
    inlineformset_factory,
)

from apps.api.models import (
    Award,
    Judge,
    Contestant,
    Score,
    Group,
    Song,
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


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = [
            'rounds',
        ]
        widgets = {
            'rounds': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
        }

    def save(self, commit=True):
        award = super(AwardForm, self).save(commit=False)
        award.build()
        if commit:
            award.save()
        return award

    def draw(self, award):
        award.draw_award()
        return award

    def start(self, award):
        award.start_award()
        return award


class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = [
            'contest',
            'person',
            'category',
            'slot',
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


# JudgeFormSet = inlineformset_factory(
#     Award,
#     Judge,
#     form=JudgeForm,
#     extra=0,
#     can_delete=False,
# )


def make_contestant_form(award):
    class ContestantForm(forms.ModelForm):
        group = forms.ModelChoiceField(
            queryset=Group.objects.filter(
                status=Group.STATUS.active,
                kind=award.kind,
            ),
        )

        class Meta:
            model = Contestant
            fields = [
                'award',
                'group',
            ]
            extra = 0
            widgets = {
                'group': forms.Select(
                    attrs={
                        'class': 'form-control',
                    },
                ),
                'award': forms.HiddenInput(
                ),
            }
    return ContestantForm


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            'song',
            'judge',
            'points',
            'status',
        ]
        extra = 0
        widgets = {
            'points': forms.TextInput(
                attrs={
                    'class': 'form-control',
                },
            ),
            'judge': forms.HiddenInput(
            ),
            'status': forms.HiddenInput(
            ),
            'song': forms.HiddenInput(
            ),
        }

ScoreFormSet = inlineformset_factory(
    Song,
    Score,
    form=ScoreForm,
    extra=0,
    can_delete=False,
)


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = [
            'performance',
            'order',
            'title',
        ]
        extra = 0
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Song Title',
                },
            ),
            'performance': forms.HiddenInput(
            ),
            'order': forms.HiddenInput(
            ),
        }
