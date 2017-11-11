# Standard Libary
import logging

from email_validator import (
    EmailNotValidError,
    validate_email,
)

# Django
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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
)

log = logging.getLogger('updater')


def update_or_create_person_from_human(human):
    first_name = human.first_name.strip()
    middle_name = human.middle_name.strip()
    last_name = human.last_name.strip()
    nick_name = human.nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
    if nick_name == first_name:
        nick_name = ""
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
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'nick_name': nick_name,
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
        person = Person.objects.get(
            bhs_pk=None,
            bhs_id=bhs_id,
        )
        person.bhs_pk = human.id
        person.save()
    except Person.DoesNotExist:
        pass
    if email:
        try:
            person = Person.objects.get(
                bhs_pk=None,
                email=email,
            )
            person.bhs_pk = human.id
            person.save()
        except Person.DoesNotExist:
            pass
    try:
        person, created = Person.objects.update_or_create(
            bhs_pk=human.id,
            defaults=defaults,
        )
    except IntegrityError as e:
        log.error("{0} {1}".format(e, human))
        return
    if created and email:
        User.objects.create_user(
            person=person,
            is_active=False,
        )
    return person, created


def update_or_create_group_from_structure(structure):
    kind_map = {
        'chapter': Group.KIND.chorus,
        'quartet': Group.KIND.quartet,
    }
    try:
        kind = kind_map[structure.kind]
    except KeyError as e:
        log.error("{0} {1}".format(e, structure))
        return
    STATUS = {
        'active': Group.STATUS.active,
        'active-internal': Group.STATUS.active,
        'active-licensed': Group.STATUS.active,
        'cancelled': Group.STATUS.inactive,
        'closed': Group.STATUS.inactive,
        'closed-merged': Group.STATUS.inactive,
        'closed-revoked': Group.STATUS.inactive,
        'closed-voluntary': Group.STATUS.inactive,
        'expelled': Group.STATUS.inactive,
        'expired': Group.STATUS.inactive,
        'expired-licensed': Group.STATUS.inactive,
        'lapsed': Group.STATUS.inactive,
        'not-approved': Group.STATUS.inactive,
        'pending': Group.STATUS.active,
        'pending-voluntary': Group.STATUS.active,
        'suspended': Group.STATUS.inactive,
        'suspended-membership': Group.STATUS.inactive,
    }
    if kind == Group.KIND.quartet:
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
    status = STATUS[str(structure.status)]
    if kind == Group.KIND.chorus:
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
    bhs_id = structure.bhs_id
    mem_status = getattr(
        Group.MEM_STATUS,
        structure.status.name.replace("-", "_")
    )
    AIC = {
        "501972": "Main Street",
        "501329": "Forefront",
        "500922": "Instant Classic",
        "304772": "Musical Island Boys",
        "500000": "Masterpiece",
        "501150": "Ringmasters",
        "317293": "Old School",
        "286100": "Storm Front",
        "500035": "Crossroads",
        "297201": "OC Times",
        "299233": "Max Q",
        "302244": "Vocal Spectrum",
        "299608": "Realtime",
        "6158": "Gotcha!",
        "2496": "Power Play",
        "276016": "Four Voices",
        "5619": "Michigan Jake",
        "6738": "Platinum",
        "3525": "FRED",
        "5721": "Revival",
        "2079": "Yesteryear",
        "2163": "Nightlife",
        "4745": "Marquis",
        "3040": "Joker's Wild",
        "1259": "Gas House Gang",
        "2850": "Keepsake",
        "1623": "The Ritz",
        "3165": "Acoustix",
        "1686": "Second Edition",
        "492": "Chiefs of Staff",
        "1596": "Interstate Rivals",
        "1654": "Rural Route 4",
        "406": "The New Tradition",
        "1411": "Rapscallions",
        "1727": "Side Street Ramblers",
        "545": "Classic Collection",
        "490": "Chicago News",
        "329": "Boston Common",
        "4034": "Grandma's Boys",
        "318": "Bluegrass Student Union",
        "362": "Most Happy Fellows",
        "1590": "Innsiders",
        "1440": "Happiness Emporium",
        "1427": "Regents",
        "627": "Dealer's Choice",
        "1288": "Golden Staters",
        "1275": "Gentlemen's Agreement",
        "709": "Oriole Four",
        "711": "Mark IV",
        "2047": "Western Continentals",
        "1110": "Four Statesmen",
        "713": "Auto Towners",
        "715": "Four Renegades",
        "1729": "Sidewinders",
        "718": "Town and Country 4",
        "719": "Gala Lads",
        "1871": "The Suntones",
        "722": "Evans Quartet",
        "724": "Four Pitchikers",
        "801366": "Gaynotes",
        "729": "Lads of Enchantment",
        "731": "Confederates",
        "732": "Four Hearsemen",
        "736": "The Orphans",
        "739": "Vikings",
        "743": "Four Teens",
        "746": "Schmitt Brothers",
        "748": "Buffalo Bills",
        "750": "Mid-States Four",
        "753": "Pittsburghers",
        "756": "Doctors of Harmony",
        "759": "Garden State Quartet",
        "761": "Misfits",
        "764": "Harmony Halls",
        "766": "Four Harmonizers",
        "770": "Elastic Four",
        "773": "Chord Busters",
        "775": "Flat Foot Four",
        "776": "Bartlesville Barflies",
    }
    if str(bhs_id) in AIC:
        status = Group.STATUS.aic
        name = AIC[str(bhs_id)]
    defaults = {
        'name': name,
        'status': status,
        'kind': kind,
        'code': code,
        'start_date': start_date,
        'email': email,
        'phone': phone,
        'bhs_id': bhs_id,
        'mem_status': mem_status,
    }
    try:
        group, created = Group.objects.update_or_create(
            bhs_pk=structure.id,
            defaults=defaults,
        )
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
    return group, created


def update_or_create_member_from_smjoin(smjoin):
    if not smjoin.status:
        # Not the canonical record
        return
    if smjoin.structure.kind == 'district':
        # Ignore districts
        return
    elif smjoin.structure.kind == 'organization':
        # Extract current Subscription from SMJoin
        person, created = update_or_create_person_from_human(smjoin.subscription.human)
        subscription = smjoin.subscription
        is_active = bool(subscription.status == 'active')
        if is_active:
            # If the subscription is active, make person active and set CT
            status = Person.STATUS.active
            current_through = subscription.current_through
        else:
            status = Person.STATUS.inactive
            current_through = None
        # set the User record to match
        try:
            person.user.is_active = is_active
            person.user.save()
        except User.DoesNotExist:
            if person.email:
                # Create a User if we have an email
                User.objects.create_user(
                    person=person,
                    is_active=is_active
                )
        person.status = status
        person.current_through = current_through
        try:
            person.full_clean()
        except ValidationError as e:
            log.error("{0} {1}".format(e, person))
            return
        person.save()
        return person, created
    elif smjoin.structure.kind in ['chapter', 'quartet']:
        # Extract current Subscription from SMJoin
        subscription = smjoin.subscription
        membership = smjoin.membership
        group, created = update_or_create_group_from_structure(smjoin.structure)
        person, created = update_or_create_person_from_human(smjoin.subscription.human)
        is_active = bool(subscription.status == 'active')
        if is_active:
            status = Member.STATUS.active
        else:
            status = Member.STATUS.inactive
        sub_status = getattr(Member.SUB_STATUS, subscription.status)
        code = getattr(Member.CODE, membership.code)
        mem_clean = membership.status.name.replace("-", "_")
        mem_status = getattr(Member.MEM_STATUS, mem_clean)
        try:
            part_clean = smjoin.vocal_part.strip().casefold()
        except AttributeError:
            part_clean = 'Unknown'
        part = getattr(Member.PART, part_clean, None)
        defaults = {
            'person': person,
            'group': group,
            'status': status,
            'part': part,
            'mem_status': mem_status,
            'sub_status': sub_status,
            'code': code,
        }
        try:
            member, created = Member.objects.update_or_create(
                bhs_pk=smjoin.id,
                defaults=defaults,
            )
        except IntegrityError as e:
            log.error("{0} {1}".format(e, smjoin))
            return
    else:
        # This is an error.
        log.error("Unknown Kind")
        return
    return member, created
