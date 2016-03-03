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
    Performance,
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


def add_judges(session, size):
    admin = Certification.objects.filter(
        category=Certification.CATEGORY.admin,
    ).order_by('?').first()
    round = session.rounds.get(num=1)
    Judge.objects.create(
        person=admin.person,
        round=round,
        category=admin.category,
        kind=Judge.KIND.official,
    )
    categories = [
        'music',
        'presentation',
        'singing',
    ]
    i = 1
    for category in categories:
        certifications = Certification.objects.filter(
            category=getattr(Certification.CATEGORY, category),
        ).order_by('?')[:size]
        for certification in certifications:
            Judge.objects.create(
                person=certification.person,
                round=round,
                slot=i,
                category=getattr(Judge.CATEGORY, category),
                kind=Judge.KIND.official,
            )
            i += 1
    return "Judges Impaneled"


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
        )
        performer.qualify()
        performer.accept()
        performer.save()
    return "Performers Added"


def add_performances(session):
    performers = session.performers.order_by('?')
    round = session.rounds.get(num=1)
    position = 0
    for performer in performers:
        Performance.objects.create(
            performer=performer,
            round=round,
            position=position,
        )
        position += 1
    return "Performances Added"


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
