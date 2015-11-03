import logging
log = logging.getLogger(__name__)

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from easy_pdf.views import PDFTemplateView

from django.contrib.auth.decorators import login_required

from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
    get_user_model,
)

from django.contrib import messages

from django.db.models import (
    Prefetch,
)

from django.forms import (
    modelformset_factory,
    inlineformset_factory,
)


from apps.api.models import (
    Contest,
    Judge,
    Session,
    Performance,
    Score,
    Song,
    Contestant,
)

from .forms import (
    LoginForm,
    ContestForm,
    ImpanelForm,
    ContestantForm,
)

User = get_user_model()


def home(request):
    if request.user.is_authenticated():
        return redirect('website:dashboard')
    else:
        return render(
            request,
            'home.html',
        )


def login(request):
    if request.method == 'POST':
        form = LoginForm(
            request.POST,
        )
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    auth_login(
                        request,
                        user,
                    )
                    messages.success(
                        request,
                        """You are logged in!"""
                    )
                    return redirect('website:home')
                else:
                    messages.error(
                        request,
                        """Your account has been closed.  Please contact Randy Meyer to reopen."""
                    )
                    return redirect('website:home')
            else:
                try:
                    user = User.objects.get(email=form.cleaned_data['email'])
                    messages.error(
                        request,
                        """That is not the correct password.  Please try again."""
                    )
                except User.DoesNotExist:
                    messages.error(
                        request,
                        """We don't recognize that email; perhaps you used a different one when you registered?"""
                    )
        else:
            for key in form.errors.keys():
                for error in form.errors[key]:
                    messages.error(
                        request,
                        error,
                    )
    else:
        form = LoginForm()
    return render(
        request,
        'registration/login.html',
        {'form': form},
    )


@login_required
def logout(request):
    auth_logout(request)
    messages.warning(
        request,
        """You are logged out""",
    )
    return redirect('website:home')


@login_required
def dashboard(request):
    contests = Contest.objects.exclude(
        status=Contest.STATUS.complete,
    )
    return render(
        request,
        'api/dashboard.html',
        {'contests': contests},
    )


@login_required
def contest(request, slug):
    contest = Contest.objects.get(
        slug=slug,
    )
    return render(
        request,
        'api/contest.html',
        {'contest': contest},
    )


@login_required
def contest_build(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    if request.method == 'POST':
        form = ContestForm(request.POST, instance=contest)
        if form.is_valid():
            form.save()
            return redirect('website:contest_impanel', contest.slug)
        else:
            for key in form.errors.keys():
                for error in form.errors[key]:
                    messages.error(
                        request,
                        error,
                    )
    else:
        form = ContestForm(instance=contest)
    return render(
        request,
        'manage/build.html',
        {'form': form},
    )


@login_required
def contest_impanel(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    JudgeFormSet = inlineformset_factory(
        Contest,
        Judge,
        form=ImpanelForm,
        extra=0,
        can_delete=False,
    )
    if request.method == 'POST':
        formset = JudgeFormSet(
            request.POST,
            instance=contest,
        )
        if formset.is_valid():
            formset.save()
            return redirect('website:contest_contestants', contest.slug)
        else:
            for key in formset.errors.keys():
                for error in formset.errors[key]:
                    messages.error(
                        request,
                        error,
                    )
    else:
        formset = JudgeFormSet(
            instance=contest,
        )
    return render(
        request,
        'manage/impanel.html',
        {'formset': formset},
    )


@login_required
def contest_contestants(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    ContestantFormSet = inlineformset_factory(
        Contest,
        Contestant,
        form=ContestantForm,
        extra=50,
        can_delete=False,
    )
    if request.method == 'POST':
        formset = ContestantFormSet(
            request.POST,
            instance=contest,
        )
        if formset.is_valid():
            formset.save()
            messages.success(
                request,
                """Contestant(s) added.""",
            )
            return redirect('website:contest_contestants', contest.slug)
        else:
            for key in formset.errors.keys():
                for error in formset.errors[key]:
                    messages.error(
                        request,
                        error,
                    )
    else:
        formset = ContestantFormSet(
            instance=contest,
        )
    return render(
        request,
        'manage/contestants.html',
        {'formset': formset},
    )


@login_required
def contest_draw(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    contestants = contest.contestants.order_by('name')
    if request.method == 'POST':
        form = ContestForm(request.POST, instance=contest)
        form.draw(contest)
        messages.warning(
            request,
            """{0} has been drawn!""".format(contest),
        )
        return redirect('website:contest_draw', contest.slug)
    else:
        form = ContestForm(instance=contest)
    return render(
        request,
        'manage/draw.html',
        {'form': form, 'contestants': contestants},
    )


@login_required
def session(request, slug):
    session = Session.objects.get(
        slug=slug,
    )
    performances = session.performances.order_by('position')
    return render(
        request,
        'api/session.html',
        {'session': session, 'performances': performances},
    )


@login_required
def performance(request, slug):
    performance = Performance.objects.get(
        slug=slug,
    )
    # songs = performance.songs.order_by('order')
    scores = Score.objects.filter(
        song__performance=performance,
    ).order_by('judge', 'song__order')
    return render(
        request,
        'api/performance.html', {
            'performance': performance,
            'scores': scores,
        },
    )


@login_required
def session_oss(request, slug):
    session = get_object_or_404(
        Session,
        slug=slug,
        # status=Session.STATUS.complete,
    )
    performances = session.performances.select_related(
        'contestant__group',
    ).prefetch_related(
        'songs',
        'songs__tune',
    ).filter(
        status=Performance.STATUS.complete,
    ).order_by(
        'place',
    )
    return render(
        request,
        'api/session_oss.html',
        {'session': session, 'performances': performances},
    )


@login_required
def contest_oss(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
        # status=Contest.STATUS.complete,
    )
    contestants = contest.contestants.select_related(
        'group',
    ).prefetch_related(
        Prefetch(
            'performances',
            queryset=Performance.objects.order_by('session__kind'),
        ),
        Prefetch(
            'performances__session',
        ),
        Prefetch(
            'performances__songs',
            queryset=Song.objects.order_by('order'),
        ),
        Prefetch('performances__songs__tune'),
    ).order_by(
        'place',
        # 'performances__session__kind',
    )
    judges = contest.judges.contest().order_by('category', 'slot',)
    winners = contest.winners.all()
    return render(
        request,
        'api/contest_oss.html',
        {'contest': contest, 'contestants': contestants, 'judges': judges, 'winners': winners},
    )


class HelloPDFView(PDFTemplateView):
    template_name = "pdf/oss.html"
    model = Contest

    def get_context_data(self, **kwargs):
            context = super(HelloPDFView, self).get_context_data(**kwargs)
            contest = get_object_or_404(
                Contest,
                slug=self.kwargs['slug'],
                # status=Contest.STATUS.complete,
            )
            contestants = contest.contestants.select_related(
                'group',
            ).prefetch_related(
                Prefetch(
                    'performances',
                    queryset=Performance.objects.order_by('session__kind'),
                ),
                Prefetch(
                    'performances__session',
                ),
                Prefetch(
                    'performances__songs',
                    queryset=Song.objects.order_by('order'),
                ),
                Prefetch('performances__songs__tune'),
            ).order_by(
                'place',
                # 'performances__session__kind',
            )
            judges = contest.judges.contest().order_by('category', 'slot',)
            winners = contest.winners.all()
            context["contest"] = contest
            context["contestants"] = contestants
            context["judges"] = judges
            context["winners"] = winners
            return context
