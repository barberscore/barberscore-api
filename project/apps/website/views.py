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
    Award,
    Round,
    Performance,
    Score,
    Song,
    Contestant,
)

from .forms import (
    make_contestant_form,
    LoginForm,
    AwardForm,
    ScoreFormSet,
    # JudgeFormSet,
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
    awards = Award.objects.exclude(
        status=Award.STATUS.final,
    )
    return render(
        request,
        'api/dashboard.html',
        {'awards': awards},
    )


@login_required
def award(request, slug):
    award = get_object_or_404(
        Award,
        slug=slug,
    )
    rounds = award.rounds.all()
    return render(
        request,
        'manage/award.html',
        {'award': award, 'rounds': rounds},
    )


@login_required
def award_build(request, slug):
    award = get_object_or_404(
        Award,
        slug=slug,
    )
    if request.method == 'POST':
        form = AwardForm(
            request.POST,
            instance=award,
        )
        if form.is_valid():
            form.save()
            return redirect('website:award_imsession', award.slug)
        else:
            for key in form.errors.keys():
                for error in form.errors[key]:
                    messages.error(
                        request,
                        error,
                    )
    else:
        form = AwardForm(
            instance=award,
        )
    return render(
        request,
        'manage/award_build.html',
        {'form': form},
    )


@login_required
def award_imsession(request, slug):
    award = get_object_or_404(
        Award,
        slug=slug,
    )
    if request.method == 'POST':
        # formset = JudgeFormSet(
        #     request.POST,
        #     instance=award,
        # )
        if formset.is_valid():
            formset.save()
            return redirect('website:award_fill', award.slug)
        else:
            for form in formset:
                for key in form.errors.keys():
                    for error in form.errors[key]:
                        messages.error(
                            request,
                            error,
                        )
    else:
        # formset = JudgeFormSet(
        #     instance=award,
        # )
        pass
    return render(
        request,
        'manage/award_imsession.html',
        {'formset': formset},
    )


@login_required
def award_fill(request, slug):
    award = get_object_or_404(
        Award,
        slug=slug,
    )
    ContestantForm = make_contestant_form(award)
    ContestantFormSet = inlineformset_factory(
        Award,
        Contestant,
        form=ContestantForm,
        extra=50,
        can_delete=False,
    )
    if request.method == 'POST':
        formset = ContestantFormSet(
            request.POST,
            instance=award,
        )
        if formset.is_valid():
            formset.save()
            messages.success(
                request,
                """Contestant(s) added.""",
            )
            return redirect('website:award_fill', award.slug)
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
            instance=award,
        )
    return render(
        request,
        'manage/award_fill.html',
        {'formset': formset},
    )


@login_required
def award_start(request, slug):
    award = get_object_or_404(
        Award,
        slug=slug,
    )
    # round = award.rounds.get(
    #     kind=award.rounds,
    # )
    # performances = round.performances.order_by('position')
    # if request.method == 'POST':
    #     form = AwardForm(request.POST, instance=award)
    #     form.start(award)
    #     messages.success(
    #         request,
    #         """The award has been started!""".format(award),
    #     )
    #     return redirect('website:round_score', round.slug)
    # else:
    #     form = AwardForm(instance=award)
    return render(
        request,
        'manage/award_start.html', {
            'award': award,
        },
    )


@login_required
def round_draw(request, slug):
    round = get_object_or_404(
        Round,
        slug=slug,
    )
    # contestants = award.contestants.order_by('name')
    # if request.method == 'POST':
    #     form = AwardForm(request.POST, instance=award)
    #     form.draw(award)
    #     messages.warning(
    #         request,
    #         """{0} has been drawn!""".format(award),
    #     )
    #     return redirect('website:award_start', award.slug)
    # else:
    #     form = AwardForm(instance=award)
    return render(
        request,
        'manage/round_draw.html',
        {'round': round},
    )


@login_required
def round_start(request, slug):
    round = get_object_or_404(
        Round,
        slug=slug,
    )
    # performances = round.performances.order_by('position')
    # if request.method == 'POST':
    #     form = AwardForm(request.POST, instance=award)
    #     form.start(award)
    #     messages.success(
    #         request,
    #         """The award has been started!""".format(award),
    #     )
    #     return redirect('website:round_score', round.slug)
    # else:
    #     form = AwardForm(instance=award)
    return render(
        request,
        'manage/round_start.html', {
            'round': round,
        },
    )


@login_required
def performance_score(request, slug):
    round = get_object_or_404(
        Round,
        slug=slug,
    )
    performance = round.performances.get(
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
                    round=round,
                    position=performance.position + 1,
                )
            except Performance.DoesNotExist:
                round.end_round()
                return redirect('website:home')
            next_performance.status = Performance.STATUS.started
            next_performance.save()
            return redirect('website:award_score', award.slug)
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
            'award': award,
            'round': round,
            'performance': performance,
            'contestant': contestant,
        },
    )


@login_required
def round_end(request, slug):
    round = Round.objects.get(slug=slug)
    return render(
        request,
        'manage/round_end.html',
        {'round': round},
    )


@login_required
def award_end(request, slug):
    award = Award.objects.get(slug=slug)
    return render(
        request,
        'manage/conetst_end.html',
        {'award': award},
    )


@login_required
def round_oss(request, slug):
    round = get_object_or_404(
        Round,
        slug=slug,
        # status=Round.STATUS.final,
    )
    performances = round.performances.select_related(
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
        'api/round_oss.html',
        {'round': round, 'performances': performances},
    )


@login_required
def award_oss(request, slug):
    award = get_object_or_404(
        Award,
        slug=slug,
        # status=Award.STATUS.final,
    )
    contestants = award.contestants.select_related(
        'group',
    ).prefetch_related(
        Prefetch(
            'performances',
            queryset=Performance.objects.order_by('round__kind'),
        ),
        Prefetch(
            'performances__round',
        ),
        Prefetch(
            'performances__songs',
            queryset=Song.objects.order_by('order'),
        ),
        Prefetch('performances__songs__tune'),
    ).order_by(
        'place',
        # 'performances__round__kind',
    )
    # judges = award.judges.official
    # competitors = award.competitors.all()
    return render(
        request,
        'api/award_oss.html', {
            'award': award,
            'contestants': contestants,
            # 'judges': judges,
            # 'competitors': competitors,
        },
    )


class HelloPDFView(PDFTemplateView):
    template_name = "pdf/oss.html"
    model = Award

    def get_context_data(self, **kwargs):
            context = super(HelloPDFView, self).get_context_data(**kwargs)
            award = get_object_or_404(
                Award,
                slug=self.kwargs['slug'],
                # status=Award.STATUS.final,
            )
            contestants = award.contestants.select_related(
                'group',
            ).prefetch_related(
                Prefetch(
                    'performances',
                    queryset=Performance.objects.order_by('round__kind'),
                ),
                Prefetch(
                    'performances__round',
                ),
                Prefetch(
                    'performances__songs',
                    queryset=Song.objects.order_by('order'),
                ),
                Prefetch('performances__songs__tune'),
            ).order_by(
                'place',
                # 'performances__round__kind',
            )
            judges = award.judges.official
            competitors = award.competitors.all()
            context["award"] = award
            context["contestants"] = contestants
            context["judges"] = judges
            context["competitors"] = competitors
            return context
