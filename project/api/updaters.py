# Standard Libary
import logging
from datetime import datetime

from django.core.validators import validate_email
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

def update_or_create_persons():
    hs = Human.objects.exclude(bhs_id=536190)
    for h in hs:
        name = h.full_name
        try:
            e_lower = h.username.lower()
            validate_email(e_lower)
            email = e_lower
        except validate_email.ValidationError:
            email = None
        birth_date = h.birth_date
        phone = h.phone
        cell_phone = h.cell_phone
        work_phone = h.work_phone
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
        person, created = Person.objects.update_or_create(
            bhs_pk=h.id,
            defaults=defaults,
        )
        print(person, created)
