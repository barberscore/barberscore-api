from django import forms

from django.forms import (
    inlineformset_factory,
)

from apps.api.models import (
    Contest,
    Judge,
    Performer,
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


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
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
        contest = super(ContestForm, self).save(commit=False)
        contest.build()
        if commit:
            contest.save()
        return contest

    def draw(self, contest):
        contest.draw_contest()
        return contest

    def start(self, contest):
        contest.start_contest()
        return contest


class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = [
            'session',
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
            'session': forms.HiddenInput(
            ),
        }


# JudgeFormSet = inlineformset_factory(
#     Contest,
#     Judge,
#     form=JudgeForm,
#     extra=0,
#     can_delete=False,
# )


def make_performer_form(contest):
    class PerformerForm(forms.ModelForm):
        group = forms.ModelChoiceField(
            queryset=Group.objects.filter(
                status=Group.STATUS.active,
                kind=contest.kind,
            ),
        )

        class Meta:
            model = Performer
            fields = [
                'contest',
                'group',
            ]
            extra = 0
            widgets = {
                'group': forms.Select(
                    attrs={
                        'class': 'form-control',
                    },
                ),
                'contest': forms.HiddenInput(
                ),
            }
    return PerformerForm


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
