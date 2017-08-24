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
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error

# Django
from django.conf import settings

# First-Party
from api.utils import get_auth0_token
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


def update_or_create_person_from_human(human):
    first_name = human.first_name.strip()
    middle_name = human.middle_name.strip()
    last_name = human.last_name.strip()
    nick_name = human.nick_name.strip()
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
        v = validate_email(human.username)
        email = v["email"].lower()
    except EmailNotValidError as e:
        email = None
    birth_date = human.birth_date
    if human.phone:
        phone = human.phone
    else:
        phone = ''
    if human.cell_phone:
        cell_phone = human.cell_phone
    else:
        cell_phone = ''
    if human.work_phone:
        work_phone = human.work_phone
    else:
        work_phone = ''
    is_bhs = True
    bhs_id = human.bhs_id
    if human.sex == 'male':
        gender = 10
    elif human.sex == 'female':
        gender = 20
    else:
        gender = None
    if human.primary_voice_part == 'Tenor':
        part = 1
    elif human.primary_voice_part == 'Lead':
        part = 2
    elif human.primary_voice_part == 'Baritone':
        part = 3
    elif human.primary_voice_part == 'Bass':
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
        'is_bhs': is_bhs,
        'bhs_id': bhs_id,
        'gender': gender,
        'part': part,
    }
    try:
        person, created = Person.objects.update_or_create(
            bhs_pk=human.id,
            defaults=defaults,
        )
        log.info((person, created))
    except IntegrityError as e:
        log.error((human, str(e)))


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
    is_bhs = True
    bhs_id = structure.bhs_id
    defaults = {
        'name': name,
        'status': status,
        'kind': kind,
        'code': code,
        'start_date': start_date,
        'email': email,
        'phone': phone,
        'is_bhs': is_bhs,
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
    if created:
        roles = Role.objects.filter(
            structure=structure,
        )
        for role in roles:
            try:
                person = Person.objects.get(
                    bhs_pk=role.human.id,
                )
            except Person.DoesNotExist as e:
                log.info(e)
                continue
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
    is_current = smjoin.status
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
    valid_through = smjoin.subscription.valid_through
    defaults = {
        'is_current': is_current,
        'valid_through': valid_through,
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
        log.error(str(e))
        return


def get_auth0():
    token = get_auth0_token()
    return Auth0(
        settings.AUTH0_DOMAIN,
        token,
    )


def get_auth0_users(auth0):
    lst = []
    more = True
    i = 0
    t = 0
    while more:
        results = auth0.users.list(
            fields=[
                'user_id',
                'email',
                'app_metadata',
                'user_metadata',
            ],
            per_page=100,
            page=i,
        )
        try:
            payload = [result for result in results['users']]
        except KeyError:
            t += 1
            if t > 3:
                break
            else:
                continue
        lst.extend(payload)
        more = bool(results['users'])
        i += 1
        t = 0
    return lst


def generate_payload(user):
    if user.person.email != user.email:
        user.email = user.person.email
        user.save()
    email = user.email

    name = user.person.nomen
    barberscore_id = str(user.id)
    payload = {
        "connection": "email",
        "email": email,
        "email_verified": True,
        "user_metadata": {
            "name": name
        },
        "app_metadata": {
            "barberscore_id": barberscore_id,
        }
    }
    return payload


def crud_auth0():
    # Get the Auth0 instance
    auth0 = get_auth0()
    # Get the accounts
    accounts = get_auth0_users(auth0)
    # Delete orphaned Auth0 accounts
    for account in accounts:
        try:
            user = User.objects.get(
                auth0_id=account['user_id'],
            )
        except User.DoesNotExist:
            auth0.users.delete(account['user_id'])
            log.info("DELETED: {0}".format(account['user_id']))
    # Get User Accounts
    users = User.objects.exclude(auth0_id=None)
    # Update each User account
    for user in users:
        # First, check to see if the User account is in the Auth0 Account list
        match = next((a for a in accounts if a['user_id'] == str(user.auth0_id)), None)
        if match:
            # If you find the account, check to see if it needs updating.
            payload = {
                'email': user.email,
                'user_metadata': {
                    'name': user.person.nomen,
                },
                'user_id': user.auth0_id,
                'app_metadata': {
                    'barberscore_id': str(user.id),
                },
            }
            if payload != match:
                # Details need updating
                del payload['user_id']
                payload['app_metadata']['bhs_id'] = None
                account = auth0.users.update(user.auth0_id, payload)
                log.info("UPDATED: {0}".format(account['user_id']))
        else:
            # The User account thinks it has an Auth0, but doesn't.  Create (reset)
            payload = generate_payload(user)
            account = auth0.users.create(payload)
            user.auth0_id = account['user_id']
            user.save()
            log.info("RESET: {0}".format(account['user_id']))
    # Create new accounts
    users = User.objects.filter(
        auth0_id=None,
    )
    for user in users:
        payload = generate_payload(user)
        # Create
        try:
            account = auth0.users.create(payload)
        except Auth0Error as e:
            log.error(e)
            continue
        user.auth0_id = account['user_id']
        user.save()
        log.info("CREATED: {0}".format(account['user_id']))


# def update_dues_thru(person):
#     try:
#         human = Human.objects.get(
#             id=person.bhs_pk,
#         )
#     except Human.DoesNotExist as e:
#         log.error(str(e))
#         return
#     try:
#         subscription = human.subscriptions.get(
#             items_editable=True,
#         )
#     except Subscription.DoesNotExist as e:
#         log.error(str(e))
#         return
#     except Subscription.MultipleObjectsReturned:
#     try:
#     subscription = human.subscriptions.get(
#     items_editable=True,
#     status='active',
#     )
#     except Subscription.DoesNotExist as e:
#     log.error(str(e))
#     return
#     except Subscription.MultipleObjectsReturned as e:
#     log.error(str(e))
#     return
#     person.dues_thru = subscription.valid_through
#     person.save()
