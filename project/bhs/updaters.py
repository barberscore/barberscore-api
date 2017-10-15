# Standard Libary
import logging

from email_validator import (
    EmailNotValidError,
    validate_email,
)

# Django
from django.db import IntegrityError
from django.utils import encoding

# First-Party
from api.models import (
    Group,
    Member,
    Organization,
    Person,
)
# Remote
from bhs.models import (
    Role,
)

log = logging.getLogger('updater')


def update_or_create_person_from_human(human):
    first_name = human.first_name.strip()
    middle_name = human.middle_name.strip()
    last_name = human.last_name.strip()
    nick_name = human.nick_name.replace("'", "").replace('"', '').strip()
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
        v = validate_email(human.email.strip())
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
    if human.sex:
        if human.sex.casefold() == 'male'.casefold():
            gender = 10
        elif human.sex.casefold() == 'female'.casefold():
            gender = 20
        else:
            gender = None
    else:
        gender = None
    if human.primary_voice_part:
        if human.primary_voice_part.casefold() == 'Tenor'.casefold():
            part = 1
        elif human.primary_voice_part.casefold() == 'Lead'.casefold():
            part = 2
        elif human.primary_voice_part.casefold() == 'Baritone'.casefold():
            part = 3
        elif human.primary_voice_part.casefold() == 'Bass'.casefold():
            part = 4
        else:
            part = None
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
    if email:
        try:
            person = Person.objects.get(email=email)
            if not person.bhs_pk:
                person.bhs_pk = human.id
                person.save()
        except Person.DoesNotExist:
            pass
    if bhs_id:
        try:
            person = Person.objects.get(bhs_id=bhs_id)
            if not person.bhs_pk:
                person.bhs_pk = human.id
                person.save()
        except Person.DoesNotExist:
            pass
    try:
        person, created = Person.objects.update_or_create(
            bhs_pk=human.id,
            defaults=defaults,
        )
        log.info((person, created))
    except IntegrityError as e:
        log.error("{0}: {1}".format(e, human))
        return


def update_or_create_group_from_structure(structure):
    kind_map = {
        'chapter': 32,
        'quartet': 41,
    }
    try:
        kind = kind_map[structure.kind]
    except KeyError as e:
        log.error("{0}: {1}".format(e, structure))
        return
    status_map = {
        'active': 10,
        'active-licensed': 10,
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
        if structure.name:
            name = structure.name.strip()
        else:
            if not structure.preferred_name:
                return
            name = "{0} (NAME APPROVAL PENDING)".format(
                structure.preferred_name.strip()
            )
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
    except EmailNotValidError:
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
        log.error("{0}: {1}".format(e, group))
        return
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
                log.error("{0}: {1}".format(e, person))
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
                log.error("{0}: {1}".format(e, member))
                return
        try:
            parent_bhs_id = structure.parent.bhs_id
        except AttributeError:
            return
        if parent_bhs_id:
            try:
                organization = Organization.objects.get(
                    bhs_id=parent_bhs_id,
                )
            except Organization.DoesNotExist:
                organization = None
            group.organization = organization
            group.save()


def update_or_create_member_from_smjoin(smjoin):
    if smjoin.structure.kind == 'district':
        # Ignore districts
        return
    if smjoin.structure.kind == 'organization':
        # Extract valid_through for Person
        subscription = smjoin.subscription
        human = smjoin.subscription.human
        try:
            person = Person.objects.get(
                bhs_pk=human.id,
            )
        except Person.DoesNotExist as e:
            log.error("{0}: {1}".format(e, human))
            return
        if subscription.status == 'active':
            status = 10
        else:
            status = -10
        valid_through = subscription.valid_through
        person.status = status
        person.valid_through = valid_through
        person.save()
        return
    if smjoin.structure.kind not in ['chapter', 'quartet']:
        # This is actually an error.
        log.error("Unknown Kind")
        return
    try:
        part_stripped = smjoin.vocal_part.strip()
    except AttributeError:
        part_stripped = None
    if part_stripped:
        if part_stripped.casefold() == 'Tenor'.casefold():
            part = 1
        elif part_stripped.casefold() == 'Lead'.casefold():
            part = 2
        elif part_stripped.casefold() == 'Baritone'.casefold():
            part = 3
        elif part_stripped.casefold() == 'Bass'.casefold():
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
        # Usually due to pending status
        log.error("{0}: {1}".format(e, smjoin))
        return
    try:
        person = Person.objects.get(
            bhs_pk=smjoin.subscription.human.id
        )
    except Person.DoesNotExist as e:
        # Generally an error
        log.error("{0}: {1}".format(e, smjoin))
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
        log.info((member, created))
    except IntegrityError as e:
        log.error("{0}: {1}".format(e, smjoin))
        return

# Potential Cruft

    # bhs = human.subscriptions.filter(
    #     items_editable=True,
    # )
    # if bhs:
    #     try:
    #         valid_through = bhs.get(
    #             status='active',
    #         ).valid_through
    #     except Subscription.DoesNotExist:
    #         # No active subscriptions; use most recent
    #         valid_through = bhs.order_by(
    #             'updated_ts',
    #         ).last().valid_through
    #     except Subscription.MultipleObjectsReturned as e:
    #         # Otherwise, bad data.
    #         log.error("{0}: {1}".format(e, human))
    #         valid_through = None
    #     if email and valid_through > datetime.date.today():
    #         status = 10
    #     else:
    #         status = -10
    # else:
    #     valid_through = None
    #     status = -10
    # if created and status == 10:
    #     try:
    #         User.objects.create_user(
    #             email=person.email,
    #             person=person,
    #         )
    #     except IntegrityError as e:
    #         log.error(e)
    #         return

    # SMJOIN
    # try:
    #     valid_through = smjoin.subscription.human.subscriptions.get(
    #         items_editable=True,
    #     ).valid_through
    # except Subscription.DoesNotExist as e:
    #     # Usually due to bad data.
    #     log.error("{0}: {1}".format(e, smjoin))
    #     return
    # except Subscription.MultipleObjectsReturned as e:
    #     try:
    #         valid_through = smjoin.subscription.human.subscriptions.get(
    #             items_editable=True,
    #             status='active',
    #         ).valid_through
    #     except Subscription.DoesNotExist as e:
    #         # Usually due to bad data.
    #         log.error("{0}: {1}".format(e, smjoin))
    #         return
    #     except Subscription.MultipleObjectsReturned as e:
    #         # Usually due to bad data.
    #         log.error("{0}: {1}".format(e, smjoin))
    #         return


# def create_user_from_person(person):
#     try:
#         v = validate_email(person.email.strip())
#         email = v["email"].lower()
#     except EmailNotValidError as e:
#         person.status = person.STATUS.inactive
#         person.save()
#         log.error("{0}: {1}".format(e, person))
#         return
#     user = User.objects.create_user(
#         email=email,
#         name=person.name,
#         person=person,
#     )
#     log.info("CREATED: {0}".format(user))
