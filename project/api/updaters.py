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
    Role,
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

    try:
        subscription = h.subscriptions.get(
            items_editable=True,
        )
    except Subscription.DoesNotExist as e:
        subscription = None
    except Subscription.MultipleObjectsReturned:
        try:
            subscription = h.subscriptions.get(
                items_editable=True,
                status='active',
            )
        except Subscription.DoesNotExist as e:
            subscription = None
        except Subscription.MultipleObjectsReturned as e:
            subscription = None
    if subscription:
        dues_thru = subscription.valid_through
    else:
        dues_thru = None
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
        'dues_thru': dues_thru,
    }
    try:
        person, created = Person.objects.update_or_create(
            bhs_pk=h.id,
            defaults=defaults,
        )
        log.info((person, created))
    except IntegrityError as e:
        log.error((h, str(e)))


def update_or_create_group_from_structure(structure):
    if not structure.name:
        return
    kind_map = {
        'chapter': 32,
        'quartet': 41,
    }
    try:
        kind = kind_map[structure.kind]
    except KeyError:
        return
    status_map = {
        'active': 10,
        'pending': 0,
        'pending-voluntary': 0,
        'expired': -10,
        'closed-revoked': -10,
        'closed-merged': -10,
        'suspended-membership': -10,
        'cancelled': -10,
        'lapsed': -10,
        'closed-voluntary': -10,
        'expelled': -10,
        'suspended': -10,
    }
    if kind == 41:
        name = structure.name.strip()
    else:
        name = "{0} [{1}]".format(
            structure.chorus_name.strip(),
            structure.name.strip(),
        )
    status = status_map[str(structure.status)]
    if kind == 32:
        code = structure.chapter_code
    else:
        code = ''
    start_date = structure.established_date
    try:
        v = validate_email(structure.email)
        email = v["email"].lower()
    except EmailNotValidError as e:
        email = ''
    if structure.phone:
        phone = structure.phone
    else:
        phone = ''
    bhs_id = structure.bhs_id
    defaults = {
        'name': name,
        'status': status,
        'kind': kind,
        'code': code,
        'start_date': start_date,
        'email': email,
        'phone': phone,
        'bhs_id': bhs_id,
    }
    try:
        group, created = Group.objects.update_or_create(
            bhs_pk=structure.id,
            defaults=defaults,
        )
        log.info((group, created))
    except IntegrityError as e:
        log.error((structure, str(e)))
    if True:
        roles = Role.objects.filter(
            structure=structure,
        )
        for role in roles:
            person = Person.objects.get(
                bhs_pk=role.human.id,
            )
            status = Member.STATUS.active
            is_admin = True
            defaults = {
                'status': status,
                'is_admin': is_admin,
            }
            try:
                member, created = Member.objects.update_or_create(
                    person=person,
                    group=group,
                    defaults=defaults,
                )
            except IntegrityError as e:
                log.error(str(e))
                return



def update_or_create_member_from_smjoin(smjoin):
    if smjoin.structure.kind not in ['chapter', 'quartet']:
        return
    try:
        part_stripped = smjoin.vocal_part.strip()
    except AttributeError:
        part_stripped = None
    if part_stripped:
        if part_stripped == 'Tenor':
            part = 1
        elif part_stripped == 'Lead':
            part = 2
        elif part_stripped == 'Baritone':
            part = 3
        elif part_stripped == 'Bass':
            part = 4
        else:
            part = None
    else:
        part = None
    if smjoin.status:
        status = 10
    else:
        status = -10
    try:
        group = Group.objects.get(
            bhs_pk=smjoin.structure.id
        )
    except Group.DoesNotExist as e:
        log.error(str(e))
        return
    try:
        person = Person.objects.get(
            bhs_pk=smjoin.subscription.human.id
        )
    except Person.DoesNotExist as e:
        log.error(str(e))
        return
    bhs_pk = smjoin.id
    defaults = {
        'status': status,
        'part': part,
        'bhs_pk': bhs_pk,
    }
    try:
        member, created = Member.objects.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
    except IntegrityError as e:
        raise(e)
        log.error(str(e))
        return
