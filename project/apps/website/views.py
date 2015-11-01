import logging
log = logging.getLogger(__name__)

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from easy_pdf.views import PDFTemplateView

from django.contrib.auth.decorators import login_required

# from django.core.urlresolvers import reverse

from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
    get_user_model,
)

# from django.contrib.auth.forms import (
#     AuthenticationForm,
# )

# from fuzzywuzzy import process

# from django.db import (
#     IntegrityError,
#     transaction,
# )

from django.contrib import messages

from django.db.models import (
    # Q,
    Prefetch,
)

# from django.core.paginator import (
#     Paginator,
#     EmptyPage,
#     PageNotAnInteger,
# )

from apps.api.models import (
    # Group,
    # Song,
    # Person,
    # Catalog,
    Contest,
    Session,
    Performance,
    Score,
    Song,
)

from .forms import (
    LoginForm,
    # MergePersonForm,
    # MergeGroupForm,
    # MergeSongForm,
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
def contest(request, contest_slug):
    contest = Contest.objects.get(
        slug=contest_slug,
    )
    return render(
        request,
        'api/contest.html',
        {'contest': contest},
    )


@login_required
def session(request, session_slug):
    session = Session.objects.get(
        slug=session_slug,
    )
    performances = session.performances.order_by('position')
    return render(
        request,
        'api/session.html',
        {'session': session, 'performances': performances},
    )


@login_required
def performance(request, performance_slug):
    performance = Performance.objects.get(
        slug=performance_slug,
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
def session_oss(request, session_slug):
    session = get_object_or_404(
        Session,
        slug=session_slug,
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
def contest_oss(request, contest_slug):
    contest = get_object_or_404(
        Contest,
        slug=contest_slug,
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

# def merge(request):
#     choruses = DuplicateGroup.objects.filter(
#         parent__kind=Group.KIND.chorus,
#     ).count()
#     quartets = DuplicateGroup.objects.filter(
#         parent__kind=Group.KIND.quartet,
#     ).count()
#     songs = DuplicateSong.objects.count()
#     persons = DuplicatePerson.objects.count()

#     return render(
#         request,
#         'merge/merge.html', {
#             'choruses': choruses,
#             'quartets': quartets,
#             'songs': songs,
#             'persons': persons,
#         },
#     )


# def all_choruses(request):s
#     groups = Group.objects.filter(
#         duplicates__isnull=False,
#     ).filter(kind=Group.KIND.chorus).distinct().order_by('name')
#     return render(
#         request,
#         'merge/all_choruses.html',
#         {'groups': groups},
#     )


# def choruses(request):
#     groups_all = Group.objects.filter(
#         duplicates__isnull=False,
#     ).filter(kind=Group.CHORUS).distinct().order_by('name')
#     paginator = Paginator(
#         groups_all,
#         1,
#     )
#     page = request.GET.get('page')
#     try:
#         groups = paginator.page(page)
#     except PageNotAnInteger:
#         groups = paginator.page(1)
#     except EmptyPage:
#         groups = paginator.page(paginator.num_pages)
#     try:
#         duplicate = groups.object_list[0].duplicates.first()
#     except IndexError:
#         duplicate = None
#     return render(
#         request,
#         'merge/choruses.html',
#         {'groups': groups, 'page': page, 'duplicate': duplicate},
#     )


# def all_quartets(request):
#     groups = Group.objects.filter(
#         duplicates__isnull=False,
#     ).filter(kind=Group.QUARTET).distinct().order_by('name')
#     return render(
#         request,
#         'merge/all_quartets.html',
#         {'groups': groups},
#     )


# def quartets(request):
#     groups_all = Group.objects.filter(
#         duplicates__isnull=False,
#     ).filter(kind=Group.QUARTET).distinct().order_by('name')
#     paginator = Paginator(
#         groups_all,
#         1,
#     )
#     page = request.GET.get('page')
#     try:
#         groups = paginator.page(page)
#     except PageNotAnInteger:
#         groups = paginator.page(1)
#     except EmptyPage:
#         groups = paginator.page(paginator.num_pages)
#     duplicate = groups.object_list[0].duplicates.first()
#     return render(
#         request,
#         'merge/quartets.html',
#         {'groups': groups, 'page': page, 'duplicate': duplicate},
#     )


# def all_songs(request):
#     songs = Song.objects.filter(
#         duplicates__isnull=False,
#     ).distinct().order_by('name')
#     return render(
#         request,
#         'merge/all_songs.html',
#         {'songs': songs},
#     )


# def songs(request):
#     songs_all = Song.objects.filter(
#         duplicates__isnull=False,
#     ).distinct().order_by('name')
#     paginator = Paginator(
#         songs_all,
#         1,
#     )
#     page = request.GET.get('page')
#     try:
#         songs = paginator.page(page)
#     except PageNotAnInteger:
#         songs = paginator.page(1)
#     except EmptyPage:
#         songs = paginator.page(paginator.num_pages)
#     duplicate = songs.object_list[0].duplicates.first()
#     return render(
#         request,
#         'merge/songs.html',
#         {'songs': songs, 'page': page, 'duplicate': duplicate},
#     )


# def all_persons(request):
#     persons = Person.objects.filter(
#         duplicates__isnull=False,
#     ).distinct().order_by('name')
#     return render(
#         request,
#         'merge/all_persons.html',
#         {'persons': persons},
#     )


# def persons(request):
#     persons_all = Person.objects.filter(
#         duplicates__isnull=False,
#     ).distinct().order_by('name')
#     paginator = Paginator(
#         persons_all,
#         1,
#     )
#     page = request.GET.get('page')
#     try:
#         persons = paginator.page(page)
#     except PageNotAnInteger:
#         persons = paginator.page(1)
#     except EmptyPage:
#         persons = paginator.page(paginator.num_pages)
#     duplicate = persons.object_list[0].duplicates.first()
#     return render(
#         request,
#         'merge/persons.html',
#         {'persons': persons, 'page': page, 'duplicate': duplicate},
#     )


# @transaction.atomic
# def merge_groups(request, parent_id, child_id):
#     parent = Group.objects.get(id=parent_id)
#     child = Group.objects.get(id=child_id)
#     if parent.kind == 1:
#         target = reverse('website:quartets')
#     else:
#         target = reverse('website:choruses')
#     page = request.GET.get('page')
#     if page:
#         target = target + "?page={0}".format(page)
#     r = redirect(target)
#     contestants = child.contestants.all()
#     # move related records
#     with transaction.atomic():
#         for contestant in contestants:
#             contestant.group = parent
#             try:
#                 contestant.save()
#             except IntegrityError:
#                 messages.error(
#                     request,
#                     u"There is a Contest conflict betwen {0} and {1}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(parent, child),
#                 )
#                 return r
#     # once records are moved, remove redundant group
#     try:
#         child.delete()
#     except Exception as e:
#         raise RuntimeError("Error deleting old group: {0}".format(e))
#     messages.success(
#         request,
#         u"Merged {0} into {1}.".format(child, parent)
#     )
#     return r


# def merge_songs(request, parent_id, child_id):
#     parent = Song.objects.get(id=parent_id)
#     child = Song.objects.get(id=child_id)
#     catalogs = child.catalogs.all()
#     target = reverse('website:songs')
#     page = request.GET.get('page')
#     if page:
#         target = target + "?page={0}".format(page)
#     r = redirect(target)
#     # move related records
#     for catalog in catalogs:
#         catalog.song = parent
#         try:
#             catalog.save()
#         except IntegrityError:
#             ps = catalog.songs.all()
#             for p in ps:
#                 p.catalog = Catalog.objects.get(
#                     song=parent,
#                     person=catalog.person,
#                 )
#                 p.save()
#     # once records are moved, remove redundant object
#     try:
#         child.delete()
#     except Exception as e:
#         raise RuntimeError("Error deleting old song: {0}".format(e))
#     messages.success(
#         request,
#         u"Merged {0} into {1}.".format(child, parent)
#     )
#     return r


# @transaction.atomic
# def merge_persons(request, parent_id, child_id):
#     parent = Person.objects.get(id=parent_id)
#     child = Person.objects.get(id=child_id)
#     quartets = child.quartets.all()
#     choruses = child.choruses.all()
#     catalogs = child.catalogs.all()
#     target = reverse('website:persons')
#     page = request.GET.get('page')
#     if page:
#         target = target + "?page={0}".format(page)
#     r = redirect(target)

#     # move related records
#     with transaction.atomic():
#         for quartet in quartets:
#             quartet.person = parent
#             try:
#                 quartet.save()
#             except IntegrityError:
#                 messages.error(
#                     request,
#                     u"There is an existing member for {0} with the name {1}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(quartet, child),
#                 )
#                 return r
#         for chorus in choruses:
#             chorus.person = parent
#             try:
#                 chorus.save()
#             except IntegrityError:
#                 messages.error(
#                     request,
#                     u"There is an existing director for {0} with the name {1}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(chorus, child),
#                 )
#                 return r
#         for catalog in catalogs:
#             catalog.person = parent
#             try:
#                 catalog.save()
#             except IntegrityError:
#                 messages.error(
#                     request,
#                     u"There is an existing catalog for {0}.  Double-check that they are in fact duplicates.  Otherwise, merge manually.".format(catalog),
#                 )
#                 return r
#     # once records are moved, remove redundant group
#     try:
#         child.delete()
#     except Exception as e:
#         raise RuntimeError("Error deleting old person: {0}".format(e))
#     messages.success(
#         request,
#         "Merged {0} into {1}.".format(child, parent)
#     )
#     return r


# def remove_group(request, parent_id):
#     parent = Group.objects.get(id=parent_id)
#     if parent.kind == Group.QUARTET:
#         target = reverse('website:quartets')
#     else:
#         target = reverse('website:choruses')
#     page = request.GET.get('page')
#     if page:
#         target = target + "?page={0}".format(page)
#     r = redirect(target)
#     duplicates = DuplicateGroup.objects.filter(
#         Q(parent=parent) | Q(child=parent)
#     )
#     duplicates.delete()
#     messages.error(
#         request,
#         u"Removed {0} from duplicates.".format(parent.name)
#     )
#     return r


# def remove_song(request, parent_id):
#     parent = Song.objects.get(id=parent_id)
#     target = reverse('website:songs')
#     page = request.GET.get('page')
#     if page:
#         target = target + "?page={0}".format(page)
#     r = redirect(target)
#     duplicates = DuplicateSong.objects.filter(
#         Q(parent=parent) | Q(child=parent)
#     )
#     duplicates.delete()
#     messages.error(
#         request,
#         u"Removed {0} from duplicates.".format(parent.name)
#     )
#     return r


# def remove_person(request, parent_id):
#     parent = Person.objects.get(id=parent_id)
#     target = reverse('website:persons')
#     page = request.GET.get('page')
#     if page:
#         target = target + "?page={0}".format(page)
#     r = redirect(target)
#     duplicates = DuplicatePerson.objects.filter(
#         Q(parent=parent) | Q(child=parent)
#     )
#     duplicates.delete()
#     messages.error(
#         request,
#         u"Removed {0} from duplicates.".format(parent.name)
#     )
#     return r


# def build_chorus():
#     vs = Group.objects.filter(kind=Group.CHORUS).values('name')
#     choices = [v['name'] for v in vs]
#     gs = Group.objects.filter(kind=Group.CHORUS)
#     i = 0
#     for g in gs:
#         i += 1
#         matches = process.extract(g.name, choices)
#         for match, score in matches:
#             if score > 85 and score < 100:
#                 child = Group.objects.get(name=match)
#                 DuplicateGroup.objects.create(
#                     parent=g,
#                     child=child,
#                     score=score,
#                 )
#         print i
#     return "Done"
#     # messages.success(
#     #     request,
#     #     "Build complete.",
#     # )
#     # return redirect('website:choruses')


# def build_quartet():
#     vs = Group.objects.filter(kind=Group.QUARTET).values('name')
#     choices = [v['name'] for v in vs]
#     gs = Group.objects.filter(kind=Group.QUARTET)
#     i = 0
#     for g in gs:
#         i += 1
#         matches = process.extract(g.name, choices)
#         for match, score in matches:
#             if score > 85 and score < 100:
#                 child = Group.objects.get(name=match)
#                 DuplicateGroup.objects.create(
#                     parent=g,
#                     child=child,
#                     score=score,
#                 )
#         print i
#     return "Done"
#     # messages.success(
#     #     request,
#     #     "Build complete.",
#     # )
#     # return redirect('website:quartets')


# def build_song():
#     vs = Song.objects.values('name')
#     choices = [v['name'] for v in vs]
#     gs = Song.objects.all()
#     i = 0
#     for g in gs:
#         i += 1
#         matches = process.extract(g.name, choices)
#         for match, score in matches:
#             if score > 85 and score < 100:
#                 child = Song.objects.get(name=match)
#                 DuplicateSong.objects.create(
#                     parent=g,
#                     child=child,
#                     score=score,
#                 )
#         print i
#     return "Done"
#     # messages.success(
#     #     request,
#     #     "Build complete.",
#     # )
#     # return redirect('website:songs')


# def build_person():
#     vs = Person.objects.values('name')
#     choices = [v['name'] for v in vs]
#     gs = Person.objects.all()
#     i = 0
#     for g in gs:
#         i += 1
#         matches = process.extract(g.name, choices)
#         for match, score in matches:
#             if score > 85 and score < 100:
#                 child = Person.objects.get(name=match)
#                 DuplicatePerson.objects.create(
#                     parent=g,
#                     child=child,
#                     score=score,
#                 )
#         print i
#     return "Done"
#     # messages.success(
#     #     request,
#     #     "Build complete.",
#     # )
#     # return redirect('website:persons')


# def manual_persons(request):
#     if request.method == 'POST':
#         form = MergePersonForm(request.POST)
#         if form.is_valid():
#             form.merge()
#             messages.success(
#                 request,
#                 "Success!! Merged {0} into {1}".format(
#                     form.cleaned_data['old'],
#                     form.cleaned_data['new'],
#                 )
#             )
#             return redirect('website:home')
#         else:
#             messages.warning(
#                 request,
#                 form.errors,
#             )
#     else:
#         form = MergePersonForm()
#     return render(
#         request,
#         'merge/manual_merge.html',
#         {'form': form},
#     )


# def manual_groups(request):
#     if request.method == 'POST':
#         form = MergeGroupForm(request.POST)
#         if form.is_valid():
#             form.merge()
#             messages.success(
#                 request,
#                 "Success!!",
#             )
#             return redirect('website:home')
#         else:
#             messages.warning(
#                 request,
#                 form.errors,
#             )
#     else:
#         form = MergeGroupForm()
#     return render(
#         request,
#         'merge/manual_merge.html',
#         {'form': form},
#     )


# def manual_songs(request):
#     if request.method == 'POST':
#         form = MergeSongForm(request.POST)
#         if form.is_valid():
#             form.merge()
#             messages.success(
#                 request,
#                 "Success!!",
#             )
#             return redirect('website:home')
#         else:
#             messages.warning(
#                 request,
#                 form.errors,
#             )
#     else:
#         form = MergeSongForm()
#     return render(
#         request,
#         'merge/manual_merge.html',
#         {'form': form},
#     )
