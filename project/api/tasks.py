# Standard Library
import logging

# Third-Party
from django_rq import job
from django.core.mail import EmailMessage

# Django
from django.template.loader import render_to_string


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


@job('high')
def send_complete_email_from_appearance(appearance):
    return appearance.send_complete_email()

@job('high')
def send_invite_email_from_entry(entry):
    return entry.send_invite_email()

@job('high')
def send_withdraw_email_from_entry(entry):
    return entry.send_withdraw_email()

@job('high')
def send_submit_email_from_entry(entry):
    return entry.send_submit_email()

@job('high')
def send_approve_email_from_entry(entry):
    return entry.send_approve_email()

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
def send_open_email_from_session(session):
    return session.send_open_email()

@job('high')
def send_close_email_from_session(session):
    return session.send_close_email()

@job('high')
def send_verify_email_from_session(session):
    return session.send_verify_email()

@job('high')
def send_verify_report_email_from_session(session):
    return session.send_verify_report_email()

@job('high')
def send_package_email_from_session(session):
    return session.send_package_email()

@job('high')
def send_package_report_email_from_session(session):
    return session.send_package_report_email()

@job('high')
def save_csa_from_appearance(appearance):
    return appearance.save_csa()

@job('high')
def save_psa_from_panelist(panelist):
    return panelist.save_psa()

@job('high')
def save_reports_from_round(round):
    return round.save_reports()

from bhs.tasks import get_auth0
@job('low')
def onetime_update_from_account(account):
    auth0 = get_auth0()
    username = account['user_id']
    name = account['user_metadata']['name']
    payload = {
        'app_metadata': {
            'name': name,
        },
        'user_metadata': {}
    }
    result = auth0.users.update(username, payload)
    return result

