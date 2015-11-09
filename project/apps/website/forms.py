from django import forms

from django.forms import (
    inlineformset_factory,
)

from apps.api.models import (
    Contest,
    Panelist,
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


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = [
            'panel',
            'rounds',
        ]
        widgets = {
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
        contest = super(ContestForm, self).save(commit=False)
        contest.build_contest()
        if commit:
            contest.save()
        return contest

    def draw(self, contest):
        contest.draw_contest()
        return contest

    def start(self, contest):
        contest.start_contest()
        return contest


class PanelistForm(forms.ModelForm):
    class Meta:
        model = Panelist
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


PanelistFormSet = inlineformset_factory(
    Contest,
    Panelist,
    form=PanelistForm,
    extra=0,
    can_delete=False,
)


def make_contestant_form(contest):
    class ContestantForm(forms.ModelForm):
        group = forms.ModelChoiceField(
            queryset=Group.objects.filter(
                status=Group.STATUS.active,
                kind=contest.kind,
            ),
        )

        class Meta:
            model = Contestant
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
    return ContestantForm


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            'song',
            'panelist',
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
            'panelist': forms.HiddenInput(
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
