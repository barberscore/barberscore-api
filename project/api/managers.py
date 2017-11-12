import logging

# Django
from django.contrib.auth.models import BaseUserManager

from email_validator import (
    EmailNotValidError,
    validate_email,
)

from django.db.models import Manager

from django.apps import apps as api_apps
config = api_apps.get_app_config('api')
bhs_config = api_apps.get_app_config('bhs')
log = logging.getLogger(__name__)


class GroupManager(Manager):

    def update_or_create_group_from_structure(self, structure, **kwargs):
        # Map structure kind to internal designation
        kind_clean = structure.kind.replace('chapter', 'chorus')
        kind = getattr(self.model.KIND, kind_clean)
        if kind == self.model.KIND.quartet:
            # Check for quartets
            if structure.name:
                # If the name has been assigned, use that.
                name = structure.name.strip()
            elif structure.preferred_name:
                # If not yet assigned, use preferred and mark as pending.
                name = "{0} (NAME APPROVAL PENDING)".format(
                    structure.preferred_name.strip()
                )
            else:
                # Otherwise, call unknown.
                name = 'UNKNOWN'
            # Quartets do not have a code.
            code = ''
        elif kind == self.model.KIND.chorus:
            # set up the chorus name
            name = "{0} [{1}]".format(
                structure.chorus_name.strip(),
                structure.name.strip(),
            )
            # And the chapter code
            code = structure.chapter_code
        else:
            raise ValueError("Can only update choruses and quartets")
        # Map to the internal designation
        STATUS = {
            'active': 'active',
            'active-internal': 'active',
            'active-licensed': 'active',
            'cancelled': 'inactive',
            'closed': 'inactive',
            'closed-merged': 'inactive',
            'closed-revoked': 'inactive',
            'closed-voluntary': 'inactive',
            'expelled': 'inactive',
            'expired': 'inactive',
            'expired-licensed': 'inactive',
            'lapsed': 'inactive',
            'not-approved': 'inactive',
            'pending': 'active',
            'pending-voluntary': 'active',
            'suspended': 'inactive',
            'suspended-membership': 'inactive',
        }
        status_clean = STATUS[str(structure.status)]
        status = getattr(self.model.STATUS, status_clean)
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
        mem_clean = structure.status.name.replace("-", "_")
        mem_status = getattr(self.model.MEM_STATUS, mem_clean)
        # Monkey-patch for the AIC
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
            status = getattr(self.model.STATUS, 'aic')
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
        group, created = self.update_or_create(
            bhs_pk=structure.id,
            defaults=defaults,
        )
        if created:
            # Set the default organization. Can be overridden in BS
            Organization = config.get_model('Organization')
            organization = Organization.objects.get(
                bhs_id=0,
            )
            group.organization = organization
            group.save()
        return group, created


class PersonManager(Manager):
    def update_or_create_person_from_human(self, human, **kwargs):
        first_name = human.first_name.strip()
        middle_name = human.middle_name.strip()
        last_name = human.last_name.strip()
        nick_name = human.nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
        if nick_name == first_name:
            nick_name = ""
        try:
            v = validate_email(human.email.strip())
            email = v["email"].lower()
        except EmailNotValidError:
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
        try:
            gender_clean = human.sex.casefold()
        except AttributeError:
            gender_clean = ""
        gender = getattr(self.model.GENDER, gender_clean, None)
        try:
            part_clean = human.primary_voice_part.casefold()
        except AttributeError:
            part_clean = ""
        part = getattr(self.model.PART, part_clean, None)
        # Set the BHS Subscription
        try:
            subscription = human.subscriptions.get(
                smjoins__structure__bhs_id=1,
                smjoins__status=True,
            )
            is_active = bool(subscription.status == 'active')
        except human.subscriptions.model.DoesNotExist:
            is_active = False
        except human.subscriptions.model.MultipleObjectsReturned:
            log.error("Multiple Canonical Joins: {0}".format(human))
            is_active = False
        if is_active:
            # If the subscription is active, make person active and set CT
            status = self.model.STATUS.active
            current_through = subscription.current_through
        else:
            status = self.model.STATUS.inactive
            current_through = None
        # Check to see if BHS ID exists already.
        try:
            # If it does, update the BHS PK
            person = self.get(
                bhs_pk=None,
                bhs_id=bhs_id,
            )
            person.bhs_pk = human.id
            person.save()
        except self.model.DoesNotExist:
            # Otherwise, continue
            pass
        # Check to see if the email exists
        if email:
            try:
                # If it does, match to PK
                person = self.get(
                    bhs_pk=None,
                    email=email,
                )
                person.bhs_pk = human.id
                person.save()
            except self.model.DoesNotExist:
                # Otherwise, continue
                pass
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
            'status': status,
            'current_through': current_through,
        }
        person, created = self.update_or_create(
            bhs_pk=human.id,
            defaults=defaults,
        )
        return person, created


class MemberManager(Manager):

    def update_or_create_member_from_join(self, join, **kwargs):
        if not join.status:
            # Check to ensure it's the right record
            raise ValueError("Must be canonical record.")
        if join.structure.kind not in ['quartet', 'chapter']:
            # Members can only be chapter or quartet.
            raise ValueError("Must be quartet or chapter record.")
        # Flatten join objects
        subscription = join.subscription
        membership = join.membership
        structure = join.structure
        human = join.subscription.human
        # Get group
        Group = config.get_model('Group')
        group, created = Group.objects.update_or_create_group_from_structure(structure)
        # Get person
        Person = config.get_model('Person')
        person, created = Person.objects.update_or_create_person_from_human(human)
        # This assumes that only 'active' matches exactly.
        status = getattr(self.model.STATUS, subscription.status, self.model.STATUS.inactive)
        # TODO perhaps add chapter voice parts?
        try:
            part_clean = join.vocal_part.strip().casefold()
        except AttributeError:
            part_clean = ''
        part = getattr(self.model.PART, part_clean, None)
        # Set the internal BHS fields
        sub_status = getattr(self.model.SUB_STATUS, subscription.status)
        code = getattr(self.model.CODE, membership.code)
        mem_clean = membership.status.name.replace("-", "_")
        mem_status = getattr(self.model.MEM_STATUS, mem_clean)
        bhs_pk = join.id
        # Set defaults and update
        defaults = {
            'status': status,
            'part': part,
            'mem_status': mem_status,
            'sub_status': sub_status,
            'code': code,
            'bhs_pk': bhs_pk,
        }
        member, created = self.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
        if created:
            # Set default admins
            Role = bhs_config.get_model('Role')
            roles = Role.objects.filter(
                human=human,
                structure=structure,
            )
            if roles:
                member.is_admin = True
            else:
                member.is_admin = True
            member.save()
        return member, created


class UserManager(BaseUserManager):

    def create_user(self, person, is_active=True, **kwargs):
        user = self.model(
            email=person.email,
            name=person.full_name,
            person=person,
            is_active=is_active,
            **kwargs
        )
        user.set_unusable_password()
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, person, password, **kwargs):
        user = self.model(
            email=email,
            name=person.full_name,
            person=person,
            is_staff=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
