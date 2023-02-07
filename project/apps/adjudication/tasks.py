# Standard Library
import logging

# Third-Party
from django_rq import job
from django.core.mail import EmailMessage

# Django
from django.template.loader import render_to_string
from django.apps import apps
from django.conf import settings

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
        if not '<' in address and not address in full:
            clean_to.append(address)
        elif not address.partition("<")[2].partition(">")[0] in full:
            clean_to.append(address)
        full.append(address.partition("<")[2].partition(">")[0])
    for address in cc:
        # print('cc address', address)
        if not '<' in address and not address in full:
            clean_cc.append(address)
        elif not address.partition("<")[2].partition(">")[0] in full:
            clean_cc.append(address)
        full.append(address.partition("<")[2].partition(">")[0])
    for address in bcc:
        if not '<' in address and not address in full:
            clean_bcc.append(address)
        elif not address.partition("<")[2].partition(">")[0] in full:
            clean_bcc.append(address)
        full.append(address.partition("<")[2].partition(">")[0])

    if (settings.EMAIL_ADMINS_ONLY):
        for address in settings.EMAIL_ADMINS:
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
    # Remove existing rounds associated with the session_id
    Round.objects.filter(session_id=session_id).delete()
    Session = apps.get_model('registration.session')
    session = Session.objects.get(id=session_id)
    session_id = session_id
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
    session_nomen = session.nomen
    session_kind = session.kind

    kind = session.num_rounds
    num = 1
    while num <= session.num_rounds:
        if num == 1:
            date = session.start_date
            spots = 10
        else:
            date = session.end_date
            spots = 0
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
        owners = session.owners.all()
        round.owners.set(owners)
        num += 1
        kind -= 1
    return


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
