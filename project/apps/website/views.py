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
    inlineformset_factory,
)


from apps.api.models import (
    Contest,
    Session,
    Performance,
    Score,
    Song,
    Contestant,
)

from .forms import (
    make_contestant_form,
    LoginForm,
    ContestForm,
    ScoreFormSet,
    PanelistFormSet,
    SongForm,
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
        status=Contest.STATUS.final,
    )
    return render(
        request,
        'api/dashboard.html',
        {'contests': contests},
    )


@login_required
def contest(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    sessions = contest.sessions.all()
    return render(
        request,
        'manage/contest.html',
        {'contest': contest, 'sessions': sessions},
    )


@login_required
def contest_build(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    if request.method == 'POST':
        form = ContestForm(
            request.POST,
            instance=contest,
        )
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
        form = ContestForm(
            instance=contest,
        )
    return render(
        request,
        'manage/contest_build.html',
        {'form': form},
    )


@login_required
def contest_impanel(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    if request.method == 'POST':
        formset = PanelistFormSet(
            request.POST,
            instance=contest,
        )
        if formset.is_valid():
            formset.save()
            return redirect('website:contest_fill', contest.slug)
        else:
            for form in formset:
                for key in form.errors.keys():
                    for error in form.errors[key]:
                        messages.error(
                            request,
                            error,
                        )
    else:
        formset = PanelistFormSet(
            instance=contest,
        )
    return render(
        request,
        'manage/contest_impanel.html',
        {'formset': formset},
    )


@login_required
def contest_fill(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    ContestantForm = make_contestant_form(contest)
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
            return redirect('website:contest_fill', contest.slug)
        else:
            for form in formset:
                for key in form.errors.keys():
                    for error in form.errors[key]:
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
        'manage/contest_fill.html',
        {'formset': formset},
    )


@login_required
def contest_start(request, slug):
    contest = get_object_or_404(
        Contest,
        slug=slug,
    )
    # session = contest.sessions.get(
    #     kind=contest.rounds,
    # )
    # performances = session.performances.order_by('position')
    # if request.method == 'POST':
    #     form = ContestForm(request.POST, instance=contest)
    #     form.start(contest)
    #     messages.success(
    #         request,
    #         """The contest has been started!""".format(contest),
    #     )
    #     return redirect('website:session_score', session.slug)
    # else:
    #     form = ContestForm(instance=contest)
    return render(
        request,
        'manage/contest_start.html', {
            'contest': contest,
        },
    )


@login_required
def session_draw(request, slug):
    session = get_object_or_404(
        Session,
        slug=slug,
    )
    # contestants = contest.contestants.order_by('name')
    # if request.method == 'POST':
    #     form = ContestForm(request.POST, instance=contest)
    #     form.draw(contest)
    #     messages.warning(
    #         request,
    #         """{0} has been drawn!""".format(contest),
    #     )
    #     return redirect('website:contest_start', contest.slug)
    # else:
    #     form = ContestForm(instance=contest)
    return render(
        request,
        'manage/session_draw.html',
        {'session': session},
    )


@login_required
def session_start(request, slug):
    session = get_object_or_404(
        Session,
        slug=slug,
    )
    # performances = session.performances.order_by('position')
    # if request.method == 'POST':
    #     form = ContestForm(request.POST, instance=contest)
    #     form.start(contest)
    #     messages.success(
    #         request,
    #         """The contest has been started!""".format(contest),
    #     )
    #     return redirect('website:session_score', session.slug)
    # else:
    #     form = ContestForm(instance=contest)
    return render(
        request,
        'manage/session_start.html', {
            'session': session,
        },
    )


@login_required
def performance_score(request, slug):
    session = get_object_or_404(
        Session,
        slug=slug,
    )
    performance = session.performances.get(
        status=Performance.STATUS.started,
    )
    contestant = performance.contestant
    song1 = performance.songs.get(order=1)
    song2 = performance.songs.get(order=2)
    if request.method == 'POST':
        songform1 = SongForm(
            request.POST,
            instance=song1,
            prefix='sf1',
        )
        songform2 = SongForm(
            request.POST,
            instance=song2,
            prefix='sf2',
        )
        formset1 = ScoreFormSet(
            request.POST,
            instance=song1,
            prefix='song1',
        )
        formset2 = ScoreFormSet(
            request.POST,
            instance=song2,
            prefix='song2',
        )
        if all([
            songform1.is_valid(),
            songform2.is_valid(),
            formset1.is_valid(),
            formset2.is_valid(),
        ]):
            songform1.save(),
            songform2.save(),
            formset1.save(),
            formset2.save(),
            # TODO plus change state, run valiations and denormalize.
            performance.end_performance()
            try:
                next_performance = Performance.objects.get(
                    session=session,
                    position=performance.position + 1,
                )
            except Performance.DoesNotExist:
                session.end_session()
                return redirect('website:home')
            next_performance.status = Performance.STATUS.started
            next_performance.save()
            return redirect('website:contest_score', contest.slug)
        else:
            for key in songform1.errors.keys():
                for error in songform1.errors[key]:
                    messages.error(
                        request,
                        error,
                    )
            for key in songform2.errors.keys():
                for error in songform2.errors[key]:
                    messages.error(
                        request,
                        error,
                    )
            for form in formset1:
                for key in form.errors.keys():
                    for error in form.errors[key]:
                        messages.error(
                            request,
                            error,
                        )
            for form in formset2:
                for key in form.errors.keys():
                    for error in form.errors[key]:
                        messages.error(
                            request,
                            error,
                        )
            formsets = [
                formset1,
                formset2,
            ]
    else:
        songform1 = SongForm(
            instance=song1,
            prefix='sf1',
        )
        songform2 = SongForm(
            instance=song2,
            prefix='sf2',
        )
        formset1 = ScoreFormSet(
            instance=song1,
            prefix='song1',
        )
        formset2 = ScoreFormSet(
            instance=song2,
            prefix='song2',
        )
        formsets = [
            formset1,
            formset2,
        ]

    return render(
        request,
        'manage/score.html', {
            'songform1': songform1,
            'songform2': songform2,
            'formsets': formsets,
            'contest': contest,
            'session': session,
            'performance': performance,
            'contestant': contestant,
        },
    )


@login_required
def session_end(request, slug):
    session = Session.objects.get(slug=slug)
    return render(
        request,
        'manage/session_end.html',
        {'session': session},
    )


@login_required
def contest_end(request, slug):
    contest = Contest.objects.get(slug=slug)
    return render(
        request,
        'manage/conetst_end.html',
        {'contest': contest},
    )


@login_required
def session_oss(request, slug):
    session = get_object_or_404(
        Session,
        slug=slug,
        # status=Session.STATUS.final,
    )
    performances = session.performances.select_related(
        'contestant__group',
    ).prefetch_related(
        'songs',
        'songs__tune',
    ).filter(
        status=Performance.STATUS.final,
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
        # status=Contest.STATUS.final,
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
    panelists = contest.panelists.official
    winners = contest.winners.all()
    return render(
        request,
        'api/contest_oss.html',
        {'contest': contest, 'contestants': contestants, 'panelists': panelists, 'winners': winners},
    )


class HelloPDFView(PDFTemplateView):
    template_name = "pdf/oss.html"
    model = Contest

    def get_context_data(self, **kwargs):
            context = super(HelloPDFView, self).get_context_data(**kwargs)
            contest = get_object_or_404(
                Contest,
                slug=self.kwargs['slug'],
                # status=Contest.STATUS.final,
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
            panelists = contest.panelists.official
            winners = contest.winners.all()
            context["contest"] = contest
            context["contestants"] = contestants
            context["panelists"] = panelists
            context["winners"] = winners
            return context
