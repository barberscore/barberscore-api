# Standard Libary
import logging

# Third-Party
from cloudinary.uploader import upload
from openpyxl import Workbook

# Django
from django.apps import apps as api_apps
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import Manager
from django.utils.timezone import now

api = api_apps.get_app_config('api')
bhs = api_apps.get_app_config('bhs')
log = logging.getLogger(__name__)

validate_url = URLValidator()

validate_twitter = RegexValidator(
    regex=r'@([A-Za-z0-9_]+)',
    message="""
        Must be a single Twitter handle
        in the form `@twitter_handle`.
    """,
)


class ChartManager(Manager):
    def export_charts(self, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'id',
            'title',
            'arrangers',
            'composers',
            'lyricists',
        ]
        ws.append(fieldnames)
        charts = self.all()
        for chart in charts:
            pk = str(chart.id)
            title = chart.title
            arrangers = chart.arrangers
            composers = chart.composers
            lyricists = chart.lyricists
            row = [
                pk,
                title,
                arrangers,
                composers,
                lyricists,
            ]
            ws.append(row)
        wb.save('barberscore_charts.xlsx')
        return upload(
            'barberscore_charts.xlsx',
            public_id='barberscore_charts.xlsx',
            resource_type='raw',
        )


class ConventionManager(Manager):
    def populate_from_last_year(self, *args, **kwargs):
        # Copy conventions, sessions, rounds, etc. from last year.
        return


class EnrollmentManager(Manager):
    def update_or_create_from_join_pks(self, join_pks, **kwargs):
        # Get group
        join__bhs_pk = join_pks[0]
        person__bhs_pk = join_pks[1]
        organization__bhs_pk = join_pks[2]
        Organization = api.get_model('Organization')
        organization = Organization.objects.get(
            bhs_pk=organization__bhs_pk,
        )
        # Get person
        Person = api.get_model('Person')
        person = Person.objects.get(
            bhs_pk=person__bhs_pk,
        )
        # Set defaults and update
        defaults = {
            'status': 10,
            'bhs_pk': join__bhs_pk,
        }
        enrollment, created = self.update_or_create(
            person=person,
            organization=organization,
            defaults=defaults,
        )
        return enrollment, created

    def update_or_create_from_join(self, join, **kwargs):
        if join.structure.kind not in ['chapter', 'quartet', ]:
            raise ValueError("Must be chapter or quartet record.")
        # Flatten join objects
        subscription = join.subscription
        membership = join.membership
        structure = join.structure
        human = join.subscription.human
        # Get group
        Organization = api.get_model('Organization')
        organization = Organization.objects.get(bhs_pk=structure.id)
        # Get person
        Person = api.get_model('Person')
        person = Person.objects.get(bhs_pk=human.id)
        # status = getattr(
        #     self.model.STATUS,
        #     subscription.status,
        #     self.model.STATUS.inactive
        # )
        status = getattr(self.model.STATUS, 'active')
        # Set the internal BHS fields
        sub_status = getattr(self.model.SUB_STATUS, subscription.status)
        mem_code = getattr(self.model.MEM_CODE, membership.code)
        mem_clean = membership.status.name.replace("-", "_")
        mem_status = getattr(self.model.MEM_STATUS, mem_clean)
        bhs_pk = join.id
        # Set defaults and update
        defaults = {
            'status': status,
            'mem_status': mem_status,
            'sub_status': sub_status,
            'mem_code': mem_code,
            'bhs_pk': bhs_pk,
        }
        enrollment, created = self.update_or_create(
            person=person,
            organization=organization,
            defaults=defaults,
        )
        return enrollment, created


class GroupManager(Manager):
    def update_or_create_from_structure(self, structure, **kwargs):
        # Map structure kind to internal designation
        kind_clean = structure.kind.replace('chapter', 'chorus')
        kind = getattr(self.model.KIND, kind_clean)
        # Check for quartets
        if kind != self.model.KIND.quartet:
            raise ValueError("Can only update quartets")
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
            'pending': 'inactive',
            'pending-voluntary': 'inactive',
            'suspended': 'inactive',
            'suspended-membership': 'inactive',
        }
        status_clean = STATUS[str(structure.status)]
        # And set the status accordingly.
        status = getattr(self.model.STATUS, status_clean)
        # Clean the raw inputs.
        email = structure.email.strip()
        try:
            validate_email(email)
        except ValidationError:
            email = ""
        phone = structure.phone.strip()
        website = structure.website.strip()
        try:
            validate_url(website)
        except ValidationError:
            website = ""
        facebook = structure.facebook.strip()
        try:
            validate_url(facebook)
        except ValidationError:
            facebook = ""
        twitter = structure.twitter.strip()
        if '@' in twitter:
            if '/' in twitter:
                twitter = twitter.rpartition("/")[2]
            else:
                twitter = twitter
        else:
            if '/' in twitter:
                twitter = twitter.rpartition('/')[2]
            else:
                twitter = "@{0}".format(twitter)
        try:
            validate_twitter(twitter)
        except ValidationError:
            twitter = ""
        bhs_id = structure.bhs_id
        start_date = structure.established_date
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
            "726": "Gaynotes",
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
            'start_date': start_date,
            'email': email,
            'phone': phone,
            'website': website,
            'facebook': facebook,
            'twitter': twitter,
            'bhs_id': bhs_id,
            'mem_status': mem_status,
        }
        group, created = self.update_or_create(
            bhs_pk=structure.id,
            defaults=defaults,
        )
        # Set the default organization on create
        if created:
            Organization = api.get_model('Organization')
            group.organization = Organization.objects.get(
                bhs_pk=structure.parent.id,
            )
            group.status = self.model.STATUS.active
            group.save()
        return group, created

    def export_active_quartets(self, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'id',
            'name',
            'bhs_id',
            'district',
        ]
        ws.append(fieldnames)
        quartets = self.filter(
            kind=self.model.KIND.quartet,
            status=self.model.STATUS.active,
        )
        for quartet in quartets:
            pk = str(quartet.id)
            name = quartet.name
            bhs_id = quartet.bhs_id
            district = str(quartet.parent)
            row = [
                pk,
                name,
                bhs_id,
                district,
            ]
            ws.append(row)
        wb.save('active_quartets.xlsx')
        return upload(
            'active_quartets.xlsx',
            public_id='active_quartets.xlsx',
            resource_type='raw',
        )


class OfficerManager(Manager):
    def update_or_create_from_role(self, role, **kwargs):
        today = now()
        if role.end_date:
            if role.end_date < today:
                status = self.model.STATUS.inactive
            else:
                status = self.model.STATUS.active
        else:
            status = self.model.STATUS.active

        # Set the internal BHS fields
        bhs_pk = role.id
        # Set defaults and update
        defaults = {
            'status': status,
        }
        officer, created = self.update_or_create(
            bhs_pk=bhs_pk,
            defaults=defaults,
        )
        return officer, created


class OrganizationManager(Manager):
    def sort_tree(self, **kwargs):
        root = self.get(kind=self.model.KIND.international)
        i = 1
        root.org_sort = i
        root.save()
        for child in root.children.order_by('kind', 'name'):
            i += 1
            child.org_sort = i
            child.save()
            for grandchild in child.children.filter(
                kind=self.model.KIND.division,
            ).order_by('kind', 'name'):
                i += 1
                grandchild.org_sort = i
                grandchild.save()
        orgs = self.filter(
            kind__in=[
                self.model.KIND.chapter,
                self.model.KIND.chorus,
                self.model.KIND.quartet,
            ]
        ).order_by(
            'kind',
            'name',
        )
        for org in orgs:
            i += 1
            org.org_sort = i
            org.save()

    def update_or_create_from_structure(self, structure, **kwargs):
        # Map structure kind to internal designation
        kind_clean = structure.kind.replace('organization', 'international')
        kind = getattr(self.model.KIND, kind_clean, None)
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
            'pending': 'inactive',
            'pending-voluntary': 'inactive',
            'suspended': 'inactive',
            'suspended-membership': 'inactive',
        }
        status_clean = STATUS[str(structure.status)]
        status = getattr(self.model.STATUS, status_clean)
        start_date = structure.established_date
        email = structure.email.strip()
        try:
            validate_email(email)
        except ValidationError:
            email = ""
        phone = structure.phone.strip()
        # And the chapter code
        if structure.chapter_code:
            code = structure.chapter_code
        else:
            code = ''
        bhs_id = structure.bhs_id
        mem_clean = structure.status.name.replace("-", "_")
        mem_status = getattr(self.model.MEM_STATUS, mem_clean)
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
        organization, created = self.update_or_create(
            bhs_pk=structure.id,
            defaults=defaults,
        )
        if created:
            # Set the default organization on create only.
            Organization = api.get_model('Organization')
            parent = Organization.objects.get(
                bhs_pk=structure.parent.id,
            )
            organization.parent = parent
            organization.status = getattr(self.model.STATUS, 'active')
            organization.save()
        return organization, created


class PersonManager(Manager):
    def update_or_create_from_human(self, human, **kwargs):
        first_name = human.first_name.strip()
        try:
            middle_name = human.middle_name.strip()
        except AttributeError:
            middle_name = ""
        last_name = human.last_name.strip()
        try:
            nick_name = human.nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
        except AttributeError:
            nick_name = ""
        if nick_name == first_name:
            nick_name = ""
        bhs_id = human.bhs_id
        email = human.email.strip()
        if email:
            try:
                validate_email(email)
            except ValidationError:
                email = ""
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
            person, created = self.update_or_create(
                bhs_pk=human.id,
                defaults=defaults,
            )
        except IntegrityError:
            defaults['bhs_pk'] = human.id
            defaults.pop('bhs_id', None)
            person, created = self.update_or_create(
                bhs_id=human.bhs_id,
                defaults=defaults,
            )
        return person, created

    def update_status_from_subscription(self, subscription, **kwargs):
        if not subscription.items_editable:
            raise ValueError("Not canonical record.")
        human = subscription.human
        person = self.get(
            bhs_pk=human.id,
        )
        status = getattr(self.model.STATUS, subscription.status, self.model.STATUS.inactive)
        current_through = subscription.current_through
        person.status = status
        person.current_through = current_through
        person.save()


class MemberManager(Manager):
    def update_or_create_from_join_pks(self, join_pks, **kwargs):
        # Get group
        join__bhs_pk = join_pks[0]
        person__bhs_pk = join_pks[1]
        group__bhs_pk = join_pks[2]
        Group = api.get_model('Group')
        group = Group.objects.get(
            bhs_pk=group__bhs_pk,
            kind=Group.KIND.quartet,
        )
        # Get person
        Person = api.get_model('Person')
        person = Person.objects.get(
            bhs_pk=person__bhs_pk,
        )
        # Set defaults and update
        defaults = {
            'status': 10,
            'bhs_pk': join__bhs_pk,
        }
        member, created = self.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
        return member, created

    def update_or_create_from_join(self, join, **kwargs):
        if join.structure.kind not in ['quartet', ]:
            raise ValueError("Must be quartet record.")
        # Flatten join objects
        subscription = join.subscription
        membership = join.membership
        structure = join.structure
        human = join.subscription.human
        # Get group
        Group = api.get_model('Group')
        group = Group.objects.get(bhs_pk=structure.id)
        # Get person
        Person = api.get_model('Person')
        person = Person.objects.get(bhs_pk=human.id)
        # status = getattr(
        #     self.model.STATUS,
        #     subscription.status,
        #     self.model.STATUS.inactive
        # )
        status = getattr(self.model.STATUS, 'active')
        try:
            part_clean = join.vocal_part.strip().casefold()
        except AttributeError:
            part_clean = ''
        part = getattr(self.model.PART, part_clean, None)
        # Set the internal BHS fields
        sub_status = getattr(self.model.SUB_STATUS, subscription.status)
        mem_code = getattr(self.model.MEM_CODE, membership.code)
        mem_clean = membership.status.name.replace("-", "_")
        mem_status = getattr(self.model.MEM_STATUS, mem_clean)
        bhs_pk = join.id
        # Set defaults and update
        defaults = {
            'status': status,
            'part': part,
            'mem_status': mem_status,
            'sub_status': sub_status,
            'mem_code': mem_code,
            'bhs_pk': bhs_pk,
        }
        member, created = self.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
        return member, created

    def update_or_create_from_enrollment(self, enrollment, **kwargs):
        # Get group
        Group = api.get_model('Group')
        group = enrollment.organization.groups.get(status=Group.STATUS.active)
        # Get person
        person = enrollment.person
        # Get fields
        status = enrollment.status
        sub_status = enrollment.sub_status
        mem_code = enrollment.mem_code
        mem_status = enrollment.mem_status
        bhs_pk = enrollment.bhs_pk
        # Set defaults and update
        defaults = {
            'status': status,
            'mem_status': mem_status,
            'sub_status': sub_status,
            'mem_code': mem_code,
            'bhs_pk': bhs_pk,
        }
        member, created = self.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
        return member, created


class UserManager(BaseUserManager):

    def create_user(self, email, is_active=True, **kwargs):
        user = self.model(
            email=email,
            is_active=is_active,
            **kwargs
        )
        user.set_unusable_password()
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
