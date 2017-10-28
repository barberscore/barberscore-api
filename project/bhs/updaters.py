# Standard Libary
import logging

from email_validator import (
    EmailNotValidError,
    validate_email,
)

# Django
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import encoding

# First-Party
from api.models import (
    Group,
    Member,
    Organization,
    Person,
    User,
)
# Remote
from bhs.models import (
    Role,
    SMJoin,
)

log = logging.getLogger('updater')


def update_or_create_person_from_human(human):
    first_name = human.first_name.strip()
    middle_name = human.middle_name.strip()
    last_name = human.last_name.strip()
    nick_name = human.nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
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
    try:
        person, created = Person.objects.update_or_create(
            bhs_pk=human.id,
            defaults=defaults,
        )
        if created and email:
            User.objects.create_user(
                person=person,
                is_active=False,
            )
        log.info("{0}; {1}".format(person, created))
    except IntegrityError as e:
        log.error("{0} {1}".format(e, human))
        return


def update_or_create_group_from_structure(structure):
    kind_map = {
        'chapter': 32,
        'quartet': 41,
    }
    try:
        kind = kind_map[structure.kind]
    except KeyError as e:
        log.error("{0} {1}".format(e, structure))
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
        log.info("{0}; {1}".format(group, created))
    except IntegrityError as e:
        log.error("{0} {1}".format(e, group))
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
                log.error("{0} {1}".format(e, person))
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
                log.error("{0} {1}".format(e, member))
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
        log.error("District mismatch")
        return
    elif smjoin.structure.kind == 'organization':
        # Must abstract this because we can't trust updated_ts
        human = smjoin.subscription.human
        smjoin = SMJoin.objects.filter(
            structure=smjoin.structure,
            subscription__human=human,
        ).order_by('established_date').last()
        # Extract current Subscription from SMJoin
        subscription = smjoin.subscription
        try:
            person = Person.objects.get(
                bhs_pk=human.id,
            )
        except Person.DoesNotExist as e:
            log.error("{0} {1}".format(e, human))
            return
        if person.email:
            if subscription.status == 'active':
                status = Person.STATUS.active
                is_valid = True
            else:
                status = Person.STATUS.inactive
                is_valid = False
        else:
            if subscription.status == 'active':
                status = Person.STATUS.missing
                is_valid = True
            else:
                status = Person.STATUS.legacy
                is_valid = False
        valid_through = subscription.valid_through
        person.status = status
        person.is_valid = is_valid
        person.valid_through = valid_through
        try:
            person.full_clean()
        except ValidationError as e:
            log.error("{0} {1}".format(e, person))
            return
        person.save()
        if status == Person.STATUS.active:
            person.user.is_active = True
            person.user.save()
        else:
            person.user.is_active = False
            person.user.save()
        log.info("{0} {1}".format(person, valid_through))
        return
    elif smjoin.structure.kind == 'chapter':
        # Must abstract this because we can't trust updated_ts
        smjoin = SMJoin.objects.filter(
            structure=smjoin.structure,
            subscription__human=smjoin.subscription.human,
        ).order_by('established_date').last()
        if smjoin.subscription.status == 'active':
            status = 10
        else:
            status = -10
        try:
            group = Group.objects.get(
                bhs_pk=smjoin.structure.id
            )
        except Group.DoesNotExist as e:
            # Probably due to pending status
            log.error("{0} {1}".format(e, smjoin))
            return
        try:
            person = Person.objects.get(
                bhs_pk=smjoin.subscription.human.id
            )
        except Person.DoesNotExist as e:
            # Generally an error
            log.error("{0} {1}".format(e, smjoin))
            return
        defaults = {
            'status': status,
        }
        try:
            member, created = Member.objects.update_or_create(
                person=person,
                group=group,
                defaults=defaults,
            )
            log.info("{0}; {1}".format(member, created))
        except IntegrityError as e:
            log.error("{0} {1}".format(e, smjoin))
            return
    elif smjoin.structure.kind == 'quartet':
        # Assumes quartets have precisely one Subscription
        smjoin = smjoin.subscription.smjoins.order_by('established_date').last()
        try:
            part_stripped = smjoin.vocal_part.strip()
        except AttributeError:
            part_stripped = "Unknown"
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
        if smjoin.subscription.status == 'active':
            status = 10
        else:
            status = -10
        try:
            group = Group.objects.get(
                bhs_pk=smjoin.structure.id
            )
        except Group.DoesNotExist as e:
            # Probably due to pending status
            log.error("{0} {1}".format(e, smjoin))
            return
        try:
            person = Person.objects.get(
                bhs_pk=smjoin.subscription.human.id
            )
        except Person.DoesNotExist as e:
            # Generally an error
            log.error("{0} {1}".format(e, smjoin))
            return
        defaults = {
            'status': status,
            'part': part,
        }
        try:
            member, created = Member.objects.update_or_create(
                person=person,
                group=group,
                defaults=defaults,
            )
            log.info("{0}; {1}".format(member, created))
        except IntegrityError as e:
            log.error("{0} {1}".format(e, smjoin))
            return
    else:
        # This is an error.
        log.error("Unknown Kind")
        return
