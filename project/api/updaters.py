# Standard Libary
import logging
from datetime import datetime

from email_validator import (
    validate_email,
    EmailNotValidError,
)

from django.db import (
    IntegrityError,
    transaction,
)
from django.utils import (
    dateparse,
    encoding,
)

# Local
from api.models import (
    Chart,
    Contestant,
    Entry,
    Group,
    Member,
    Office,
    Officer,
    Participant,
    Person,
    Repertory,
    Session,
    User,
)

# Remote
from bhs.models import (
    Human,
    Membership,
    Status,
    Structure,
    Subscription,
)

log = logging.getLogger('updater')

def update_or_create_person_from_human(h):
    first_name = h.first_name.strip()
    middle_name = h.middle_name.strip()
    last_name = h.last_name.strip()
    nick_name = h.nick_name.strip()
    if not first_name:
        first_name = None
    if not middle_name:
        middle_name = None
    if not last_name:
        last_name = None
    if nick_name and (nick_name != first_name):
        nick_name = "({0})".format(nick_name)
    else:
        nick_name = None
    name = " ".join(
        map(
            (lambda x: encoding.smart_text(x)),
            filter(
                None, [
                    first_name,
                    middle_name,
                    last_name,
                    nick_name,
                ]
            )
        )
    )
    try:
        v = validate_email(h.username)
        email = v["email"].lower()
    except EmailNotValidError as e:
        email = None
    birth_date = h.birth_date
    if h.phone:
        phone = h.phone
    else:
        phone = ''
    if h.cell_phone:
        cell_phone = h.cell_phone
    else:
        cell_phone = ''
    if h.work_phone:
        work_phone = h.work_phone
    else:
        work_phone = ''
    bhs_id = h.bhs_id
    if h.sex == 'male':
        gender = 10
    elif h.sex == 'female':
        gender = 20
    else:
        gender = None
    if h.primary_voice_part == 'Tenor':
        part = 1
    elif h.primary_voice_part == 'Lead':
        part = 2
    elif h.primary_voice_part == 'Baritone':
        part = 3
    elif h.primary_voice_part == 'Bass':
        part = 4
    else:
        part = None
    defaults = {
        'name': name,
        'email': email,
        'birth_date': birth_date,
        'phone': phone,
        'cell_phone': cell_phone,
        'work_phone': work_phone,
        'bhs_id': bhs_id,
        'gender': gender,
        'part': part,
    }
    try:
        person, created = Person.objects.update_or_create(
            bhs_pk=h.id,
            defaults=defaults,
        )
        log.info((person, created))
    except IntegrityError as e:
        log.error((h, str(e)))
