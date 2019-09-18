# Standard Library
import logging

# Third-Party
from django_rq import job
from django.core.mail import EmailMessage

# Django
from django.template.loader import render_to_string
from django.apps import apps

log = logging.getLogger(__name__)

# Utility
def build_email(template, context, subject, to, cc=[], bcc=[], attachments=[]):
    # Clean as necessary
    # Remove commas
    to = [x.replace(",", "") for x in to]
    cc = [x.replace(",", "") for x in cc]
    bcc = [x.replace(",", "") for x in bcc]

    # Remove duplicate emails, keeping only the first
    full = []
    clean_to = []
    clean_cc = []
    clean_bcc = []
    for address in to:
        if not address.partition("<")[2].partition(">")[0] in full:
            clean_to.append(address)
        full.append(address.partition("<")[2].partition(">")[0])
    for address in cc:
        if not address.partition("<")[2].partition(">")[0] in full:
            clean_cc.append(address)
        full.append(address.partition("<")[2].partition(">")[0])
    for address in bcc:
        if not address.partition("<")[2].partition(">")[0] in full:
            clean_bcc.append(address)
        full.append(address.partition("<")[2].partition(">")[0])

    body = render_to_string(template, context)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='Barberscore <admin@barberscore.com>',
        to=clean_to,
        cc=clean_cc,
        bcc=clean_bcc,
    )
    for attachment in attachments:
        with attachment[1].open() as f:
            email.attach(attachment[0], f.read(), attachment[2])
    return email


def build_rounds_from_session(session_id):
    Round = apps.get_model('adjudication.round')
    Session = apps.get_model('registration.session')
    Assignment = apps.get_model('registration.assignment')
    Entry = apps.get_model('registration.entry')
    session = Session.objects.get(id=session_id)
    kind = session.num_rounds
    num = 1
    spots = 10
    date = session.start_date
    convention_id = session.convention_id
    name = session.name
    district = session.district
    season = session.season
    panel = session.panel
    year = session.year
    open_date = session.open_date
    close_date = session.close_date
    start_date = session.start_date
    end_date = session.end_date
    venue_name = session.venue_name
    location = session.location
    timezone = session.timezone
    divisions = session.divisions
    image_id = session.image_id
    session_id = str(session.id)
    session_nomen = session.nomen
    session_kind = session.kind
    owners = session.owners.all()
    contests = session.contests.filter(
        entries__isnull=False,
    ).order_by(
        'tree_sort',
    ).distinct()
    cas = session.assignments.filter(
        category=Assignment.CATEGORY.ca,
    ).order_by(
        'kind',
        'category',
        'last_name',
        'first_name',
    )
    judges = session.assignments.filter(
        category__in=[
            Assignment.CATEGORY.singing,
            Assignment.CATEGORY.performance,
            Assignment.CATEGORY.music,
        ],
        kind=Assignment.KIND.official,
    ).order_by(
        'kind',
        'category',
        'last_name',
        'first_name',
    )
    practices = session.assignments.filter(
        category__in=[
            Assignment.CATEGORY.singing,
            Assignment.CATEGORY.performance,
            Assignment.CATEGORY.music,
        ],
        kind=Assignment.KIND.practice,
    ).order_by(
        'kind',
        'category',
        'last_name',
        'first_name',
    )
    entries = session.entries.filter(
        status=Entry.STATUS.approved,
    ).order_by('draw')
    round = Round.objects.create(
        kind=kind,
        num=num,
        spots=spots,
        date=date,
        convention_id=convention_id,
        name=name,
        district=district,
        season=season,
        panel=panel,
        year=year,
        open_date=open_date,
        close_date=close_date,
        start_date=start_date,
        end_date=end_date,
        venue_name=venue_name,
        location=location,
        timezone=timezone,
        divisions=divisions,
        image_id=image_id,
        session_id=session_id,
        session_nomen=session_nomen,
        session_kind=session_kind,
    )
    round.owners.set(owners)
    # return round
    i = 0
    for contest in contests:
        i += 1
        round.outcomes.create(
            num=i,
            award_id=contest.award_id,
            name=contest.name,
            kind=contest.kind,
            gender=contest.gender,
            level=contest.level,
            season=contest.season,
            district=contest.district,
            division=contest.division,
            age=contest.age,
            is_novice=contest.is_novice,
        )
    for entry in entries:
        is_single = bool(entry.contests.filter(
            is_single=False,
        ))
        round.appearances.create(
            num=entry.draw,
            is_private=entry.is_private,
            is_single=is_single,
            participants=entry.participants,
            district=entry.district,
        )
    for ca in cas:
        area = ca.get_district_display() if ca.district else ''
        round.panelists.create(
            kind=ca.kind,
            category=ca.category,
            person_id=ca.person_id,
            name=ca.name,
            first_name=ca.first_name,
            last_name=ca.last_name,
            area=area,
            email=ca.email,
            cell_phone=ca.cell_phone,
            bhs_id=ca.bhs_id,
        )

    i = 0
    for judge in judges:
        i += 1
        area = judge.get_district_display() if judge.district else ''
        round.panelists.create(
            num=i,
            kind=judge.kind,
            category=judge.category,
            person_id=judge.person_id,
            name=judge.name,
            first_name=judge.first_name,
            last_name=judge.last_name,
            area=area,
            email=judge.email,
            cell_phone=judge.cell_phone,
            bhs_id=judge.bhs_id,
        )
    i = 50
    for practice in practices:
        i += 1
        area = practice.get_district_display() if practice.district else ''
        round.panelists.create(
            num=i,
            kind=practice.kind,
            category=practice.category,
            person_id=practice.person_id,
            name=practice.name,
            first_name=practice.first_name,
            last_name=practice.last_name,
            area=area,
            email=practice.email,
            cell_phone=practice.cell_phone,
            bhs_id=practice.bhs_id,
        )


@job('high')
def send_complete_email_from_appearance(appearance):
    return appearance.send_complete_email()


@job('high')
def send_psa_email_from_panelist(panelist):
    return panelist.send_psa_email()

@job('high')
def send_publish_email_from_round(round):
    return round.send_publish_email()

@job('high')
def send_publish_report_email_from_round(round):
    return round.send_publish_report_email()

@job('high')
def save_csa_from_appearance(appearance):
    return appearance.save_csa()

@job('high')
def save_psa_from_panelist(panelist):
    return panelist.save_psa()

@job('high')
def save_reports_from_round(round):
    return round.save_reports()
