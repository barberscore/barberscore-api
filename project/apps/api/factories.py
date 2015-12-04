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
    Contest,
    Certification,
    Tune,
    Judge,
    Competitor,
    Session,
)


def add_sessions(contest):
    # TODO Wonky.  Do these need kinds?
    rounds = contest.rounds
    k = rounds
    i = 1
    while i <= rounds:
        Session.objects.create(
            contest=contest,
            num=i,
            kind=k,
        )
        i += 1
        k -= 1


def add_judges(contest):
    size = contest.size
    admin = Certification.objects.filter(
        category=Certification.CATEGORY.admin,
    ).order_by('?').first()
    Judge.objects.create(
        person=admin.person,
        contest=contest,
        slot=1,
        kind=admin.category,
    )
    # TODO This is not very DRY...
    musics = Certification.objects.filter(
        category=Certification.CATEGORY.music,
    ).order_by('?')[:size]
    i = 1
    for music in musics:
        Judge.objects.create(
            person=music.person,
            contest=contest,
            slot=i,
            kind=music.category,
        )
        i += 1
    presentations = Certification.objects.filter(
        category=Certification.CATEGORY.presentation,
    ).order_by('?')[:size]
    i = 1
    for presentation in presentations:
        Judge.objects.create(
            person=presentation.person,
            contest=contest,
            slot=i,
            kind=presentation.category,
        )
        i += 1
    singings = Certification.objects.filter(
        category=Certification.CATEGORY.singing,
    ).order_by('?')[:size]
    i = 1
    for singing in singings:
        Judge.objects.create(
            person=singing.person,
            contest=contest,
            slot=i,
            kind=singing.category,
        )
        i += 1
    return "Judges Imcontested"


def add_contestants(contest, number=20):
    if contest.kind == Contest.KIND.chorus:
        kind = Group.KIND.chorus
    else:
        kind = Group.KIND.quartet
    groups = Group.objects.filter(
        kind=kind,
        status=Group.STATUS.active,
    ).order_by('?')[:number]
    for group in groups:
        contestant = Contestant.objects.create(
            contest=contest,
            group=group,
            prelim=randint(700, 900) * .1,
        )
        contestant.qualify()
        contestant.accept()
        contestant.save()
    return "Contestants Added"


def add_competitors(award, number=10):
    contestants = award.contest.contestants.order_by('?')[:number]
    for contestant in contestants:
        Competitor.objects.create(
            award=award,
            contestant=contestant,
        )
    return "Competitors Added"


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
