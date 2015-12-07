from random import (
    randint,
)

from django.utils import timezone

from factory.django import (
    DjangoModelFactory,
)

from .models import (
    Certification,
    Contestant,
    Session,
    Performer,
    Group,
    Judge,
    Round,
    Tune,
)


def add_rounds(session):
    # TODO Wonky.  Do these need kinds?
    rounds = session.rounds
    k = rounds
    i = 1
    while i <= rounds:
        Round.objects.create(
            session=session,
            num=i,
            kind=k,
        )
        i += 1
        k -= 1


def add_judges(session):
    size = session.size
    admin = Certification.objects.filter(
        category=Certification.CATEGORY.admin,
    ).order_by('?').first()
    Judge.objects.create(
        person=admin.person,
        session=session,
        slot=1,
        category=admin.category,
        kind=Judge.KIND.official,
    )
    # TODO This is not very DRY...
    musics = Certification.objects.filter(
        category=Certification.CATEGORY.music,
    ).order_by('?')[:size]
    i = 1
    for music in musics:
        Judge.objects.create(
            person=music.person,
            session=session,
            slot=i,
            category=music.category,
            kind=Judge.KIND.official,
        )
        i += 1
    presentations = Certification.objects.filter(
        category=Certification.CATEGORY.presentation,
    ).order_by('?')[:size]
    i = 1
    for presentation in presentations:
        Judge.objects.create(
            person=presentation.person,
            session=session,
            slot=i,
            category=presentation.category,
            kind=Judge.KIND.official,
        )
        i += 1
    singings = Certification.objects.filter(
        category=Certification.CATEGORY.singing,
    ).order_by('?')[:size]
    i = 1
    for singing in singings:
        Judge.objects.create(
            person=singing.person,
            session=session,
            slot=i,
            category=singing.category,
            kind=Judge.KIND.official,
        )
        i += 1
    return "Judges Imsessioned"


def add_performers(session, number=20):
    if session.kind == Session.KIND.chorus:
        kind = Group.KIND.chorus
    else:
        kind = Group.KIND.quartet
    groups = Group.objects.filter(
        kind=kind,
        status=Group.STATUS.active,
    ).order_by('?')[:number]
    for group in groups:
        performer = Performer.objects.create(
            session=session,
            group=group,
            prelim=randint(700, 900) * .1,
        )
        performer.qualify()
        performer.accept()
        performer.save()
    return "Performers Added"


def add_contestants(contest, number=10):
    performers = contest.session.performers.order_by('?')[:number]
    for performer in performers:
        Contestant.objects.create(
            contest=contest,
            performer=performer,
        )
    return "Contestants Added"


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


def schedule_performances(round):
    performances = round.performances.all()
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
