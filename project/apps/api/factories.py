from random import (
    randint,
)

from django.utils import timezone

from factory.django import (
    DjangoModelFactory,
)

from .models import (
    Group,
    Contestant,
    Certification,
    Tune,
    Panelist,
    Ranking,
    Session,
)


def add_sessions(panel):
    # TODO Wonky.  Do these need kinds?
    rounds = panel.rounds
    k = rounds
    i = 1
    while i <= rounds:
        Session.objects.create(
            panel=panel,
            num=i,
            kind=k,
        )
        i += 1
        k -= 1


def add_panelists(panel):
    size = panel.size
    admin = Certification.objects.filter(
        category=Certification.CATEGORY.admin,
    ).order_by('?').first()
    Panelist.objects.create(
        person=admin.person,
        panel=panel,
        slot=1,
        kind=admin.category,
    )
    # TODO This is not very DRY...
    musics = Certification.objects.filter(
        category=Certification.CATEGORY.music,
    ).order_by('?')[:size]
    i = 1
    for music in musics:
        Panelist.objects.create(
            person=music.person,
            panel=panel,
            slot=i,
            kind=music.category,
        )
        i += 1
    presentations = Certification.objects.filter(
        category=Certification.CATEGORY.presentation,
    ).order_by('?')[:size]
    i = 1
    for presentation in presentations:
        Panelist.objects.create(
            person=presentation.person,
            panel=panel,
            slot=i,
            kind=presentation.category,
        )
        i += 1
    singings = Certification.objects.filter(
        category=Certification.CATEGORY.singing,
    ).order_by('?')[:size]
    i = 1
    for singing in singings:
        Panelist.objects.create(
            person=singing.person,
            panel=panel,
            slot=i,
            kind=singing.category,
        )
        i += 1
    return "Panelists Impaneled"


def add_contestants(convention, kind=Group.KIND.quartet, number=20):
    groups = Group.objects.filter(
        kind=kind,
        status=Group.STATUS.active,
    ).order_by('?')[:number]
    for group in groups:
        contestant = Contestant.objects.create(
            convention=convention,
            group=group,
            # prelim=randint(700, 900) * .1,
        )
        contestant.qualify()
        contestant.accept()
        contestant.save()
    return "Contestants Added"


def add_rankings(contest, number=10):
    contestants = contest.convention.contestants.order_by('?')[:number]
    for contestant in contestants:
        Ranking.objects.create(
            contest=contest,
            contestant=contestant,
        )
    return "Rankings Added"


def score_performance(performance):
    base = randint(70, 90)
    songs = performance.songs.all()
    for song in songs:
        song.title = Tune.objects.order_by('?').first().name
        scores = song.scores.all()
        for score in scores:
            low, high = base, base + 5
            score.points = randint(low, high)
            score.save()
        song.save()
    performance.save()
    return "Performance Scored"


def schedule_performances(session):
    performances = session.performances.all()
    for performance in performances:
        performance.start_time = timezone.now()
        performance.prep()
        performance.save()
    return "Performances scheduled"


class QuartetFactory(DjangoModelFactory):
    name = "The Buffalo Bills"
    kind = Group.KIND.quartet

    class Meta:
        model = Group
