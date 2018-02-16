# Standard Libary
import logging
import django_rq

# Third-Party
from cloudinary.uploader import upload
from openpyxl import Workbook

# Django
from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import Manager
from django.utils.timezone import now
from api.tasks import get_accounts
from api.tasks import update_or_create_account_from_user
from api.tasks import delete_account


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


class GroupManager(Manager):
    def update_or_create_from_structure(self, structure, **kwargs):
        # Map structure kind to internal designation
        kind_clean = structure.kind.replace('chapter', 'chorus')
        kind = getattr(self.model.KIND, kind_clean)
        # Check for quartets
        if kind == self.model.KIND.quartet:
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
        elif kind == self.model.KIND.chorus:
            if structure.chorus_name:
                name = structure.chorus_name.strip()
            else:
                name = 'UNKNOWN'
        else:
            raise ValueError("Must be quartet or chapter")
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
        # Set defaults on create
        if created:
            if kind == self.model.KIND.quartet:
                group.is_senior = group.get_is_senior()
            if kind == self.model.KIND.chorus:
                log.error("New Chorus: {0}".format(group))
                group.status = self.model.STATUS.new
                group.save()
                return group, created
            parent = self.get(bhs_pk=structure.parent.id)
            group.parent = parent
            group.status = self.model.STATUS.new
            group.save()
        return group, created

    def update_or_create_from_structure_object(self, structure, **kwargs):
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
        # Map to incoming
        bhs_pk = structure[0]
        name = structure[1]
        preferred_name = structure[2]
        chorus_name = structure[3]
        status = getattr(self.model.STATUS, STATUS[str(structure[4])])
        kind = getattr(self.model.KIND, structure[5].replace('chapter', 'chorus'))
        start_date = structure[6]
        email = structure[7]
        phone = structure[8]
        website = structure[9]
        facebook = structure[10]
        twitter = structure[11]
        bhs_id = structure[12]
        parent = structure[13]
        mem_status = getattr(self.model.MEM_STATUS, structure[4].replace("-", "_"))

        if kind == self.model.KIND.quartet:
            if name:
                # If the name has been assigned, use that.
                name = name.strip()
            elif preferred_name:
                # If not yet assigned, use preferred and mark as pending.
                name = "{0} (NAME APPROVAL PENDING)".format(
                    preferred_name.strip()
                )
            else:
                # Otherwise, call unknown.
                name = 'UNKNOWN'
            # Map to the internal designation
        elif kind == self.model.KIND.chorus:
            if chorus_name:
                name = chorus_name.strip()
            else:
                name = 'UNKNOWN'
        else:
            raise ValueError("Must be quartet or chapter")
        # Clean the raw inputs.
        email = email.strip()
        try:
            validate_email(email)
        except ValidationError:
            email = ""
        phone = phone.strip()
        website = website.strip()
        try:
            validate_url(website)
        except ValidationError:
            website = ""
        facebook = facebook.strip()
        try:
            validate_url(facebook)
        except ValidationError:
            facebook = ""
        twitter = twitter.strip()
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
        # Monkey-patch for the AIC
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
            bhs_pk=bhs_pk,
            defaults=defaults,
        )
        # Set defaults on create
        if created:
            if kind == self.model.KIND.quartet:
                group.is_senior = group.get_is_senior()
            if kind == self.model.KIND.chorus:
                log.error("New Chorus: {0}".format(group))
                group.status = self.model.STATUS.new
                group.save()
                return group, created
            parent = self.get(bhs_pk=parent)
            group.parent = parent
            group.status = self.model.STATUS.new
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

    def sort_tree(self, **kwargs):
        root = self.get(kind=self.model.KIND.international)
        i = 1
        root.tree_sort = i
        root.save()
        for child in root.children.order_by('kind', 'name'):
            i += 1
            child.tree_sort = i
            child.save()
            for grandchild in child.children.filter(
                kind=self.model.KIND.division,
            ).order_by('kind', 'name'):
                i += 1
                grandchild.tree_sort = i
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
            org.tree_sort = i
            org.save()
        return


class OfficerManager(Manager):
    def update_or_create_from_role(self, role, **kwargs):
        today = now().date()
        if role.end_date:
            if role.end_date < today:
                status = self.model.STATUS.inactive
            else:
                status = self.model.STATUS.active
        else:
            status = self.model.STATUS.active

        # Flatten join objects
        structure = role.structure
        human = role.human
        name = role.name
        # Get group
        Group = apps.get_model('api.group')
        group = Group.objects.get(bhs_pk=structure.id)
        # Get person
        Person = apps.get_model('api.person')
        person = Person.objects.get(bhs_pk=human.id)
        # Get office
        Office = apps.get_model('api.office')
        office = Office.objects.get(name=name)

        # Set the internal BHS fields
        bhs_pk = role.id
        # Set defaults and update
        defaults = {
            'status': status,
            'group': group,
            'person': person,
            'office': office,
        }
        officer, created = self.update_or_create(
            bhs_pk=bhs_pk,
            defaults=defaults,
        )
        return officer, created

    def update_or_create_from_role_object(self, role, **kwargs):
        today = now().date()
        bhs_pk = role[0]
        office = role[1]
        group = role[2]
        person = role[3]
        start_date = role[4]
        end_date = role[5]

        if end_date:
            if end_date < today:
                status = self.model.STATUS.inactive
            else:
                status = self.model.STATUS.active
        else:
            status = self.model.STATUS.active

        # Get group
        Group = apps.get_model('api.group')
        group = Group.objects.get(bhs_pk=group)
        # Get person
        Person = apps.get_model('api.person')
        person = Person.objects.get(bhs_pk=person)
        # Get office
        Office = apps.get_model('api.office')
        office = Office.objects.get(name=office)

        # Set defaults and update
        defaults = {
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
            'bhs_pk': bhs_pk,
        }
        officer, created = self.update_or_create(
            person=person,
            group=group,
            office=office,
            defaults=defaults,
        )
        return officer, created

    def update_or_create_from_member(self, member, **kwargs):
        if member.group.kind != member.group.KIND.quartet:
            raise ValueError("Must be quartet record.")
        # Flatten join objects
        # Get group
        if member.status > 0:
            status = self.model.STATUS.active
        elif member.status < 0:
            status = self.model.STATUS.inactive
        else:
            status = 0
        bhs_pk = None
        # Get office
        Office = apps.get_model('api.office')
        office = Office.objects.get(name='Quartet Manager')
        # Set defaults and update
        defaults = {
            'status': status,
            'bhs_pk': bhs_pk,
        }
        officer, created = self.update_or_create(
            person=member.person,
            group=member.group,
            office=office,
            defaults=defaults,
        )
        return officer, created

    def update_or_create_from_join_object(self, join, **kwargs):
        bhs_pk = join[0]
        status = join[1]
        group = join[2]
        person = join[3]

        if status:
            status = self.model.STATUS.active
        else:
            status = self.model.STATUS.inactive

        # Get group
        Group = apps.get_model('api.group')
        group = Group.objects.get(bhs_pk=group)
        # Get person
        Person = apps.get_model('api.person')
        person = Person.objects.get(bhs_pk=person)
        # Get office
        Office = apps.get_model('api.office')
        office = Office.objects.get(name='Quartet Manager')

        # Set defaults and update
        defaults = {
            'status': status,
            'bhs_pk': bhs_pk,
        }
        officer, created = self.update_or_create(
            person=person,
            group=group,
            office=office,
            defaults=defaults,
        )
        return officer, created


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
        status = self.model.STATUS.inactive
        defaults = {
            'status': status,
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

    def update_or_create_from_human_object(self, human, **kwargs):
        bhs_pk = human[0]
        first_name = human[1]
        middle_name = human[2]
        last_name = human[3]
        nick_name = human[4]
        email = human[5]
        birth_date = human[6]
        phone = human[7]
        cell_phone = human[8]
        work_phone = human[9]
        bhs_id = human[10]
        gender = human[11]
        part = human[12]

        first_name = first_name.strip()
        try:
            middle_name = middle_name.strip()
        except AttributeError:
            middle_name = ""
        last_name = last_name.strip()
        try:
            nick_name = nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
        except AttributeError:
            nick_name = ""
        if nick_name == first_name:
            nick_name = ""
        if email:
            email = email.strip()
            try:
                validate_email(email)
            except ValidationError:
                email = None
        else:
            email = None
        if not phone:
            phone = ''
        if not cell_phone:
            cell_phone = ''
        if not work_phone:
            work_phone = ''
        if gender:
            gender = getattr(self.model.GENDER, gender.casefold(), None)
        else:
            gender = None
        if part:
            part = getattr(self.model.PART, part.casefold(), None)
        else:
            part = None
        # Set default; subscriptions updates it.
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
                bhs_pk=bhs_pk,
                defaults=defaults,
            )
        except IntegrityError:
            defaults['bhs_pk'] = bhs_pk
            defaults.pop('bhs_id', None)
            person, created = self.update_or_create(
                bhs_id=bhs_id,
                defaults=defaults,
            )
        if created:
            # Subscription overwrites, set default
            person.status = self.model.STATUS.inactive
            person.save()
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

    def update_status_from_subscription_object(self, subscription, **kwargs):
        items_editable = subscription[1]
        if not items_editable:
            raise ValueError("Not canonical record")
        bhs_pk = subscription[0]
        status = getattr(self.model.STATUS, subscription[2], self.model.STATUS.inactive)
        current_through = subscription[3]
        if not subscription[1]:
            raise ValueError("Not canonical record.")
        person = self.get(
            bhs_pk=bhs_pk,
        )
        person.status = status
        person.current_through = current_through
        person.save()

    def update_users(self, cursor=None, *args, **kwargs):
        # Get Base
        persons = self.filter(
            email__isnull=False,
        )
        if cursor:
            persons = persons.filter(
                modified__gt=cursor,
            )
        # Return as objects
        # persons = persons.values_list(
        #     'id',
        #     'nomen',
        #     'email',
        #     'status',
        # )
        User = apps.get_model('api.user')
        for person in persons:
            django_rq.enqueue(
                User.objects.update_or_create_from_person,
                person,
            )
        return persons.count()


class MemberManager(Manager):
    def update_or_create_from_join_object(self, join, **kwargs):
        # Get group
        bhs_pk = join[0]
        Group = apps.get_model('api.group')
        group = Group.objects.get(
            bhs_pk=join[1],
            kind__in=[
                Group.KIND.quartet,
                Group.KIND.chorus,
            ]
        )
        # Get person
        Person = apps.get_model('api.person')
        person = Person.objects.get(
            bhs_pk=join[2],
        )
        if join[3]:
            status = self.model.STATUS.active
        else:
            status = self.model.STATUS.inactive
        if join[8]:
            part = getattr(
                self.model.PART,
                join[8].lower(),
                None,
            )
        else:
            part = None
        inactive_date = join[4]
        # Set the internal BHS fields
        if join[5]:
            inactive_reason = getattr(
                self.model.INACTIVE_REASON,
                join[5].replace("-", "_").replace(" ", ""),
                None,
            )
        else:
            inactive_reason = None
        mem_status = getattr(
            self.model.MEM_STATUS,
            join[6].replace("-", "_"),
            None
        )
        mem_code = getattr(self.model.MEM_CODE, join[7], None)
        # Set defaults and update
        defaults = {
            'status': status,
            'part': part,
            'mem_status': mem_status,
            'mem_code': mem_code,
            'inactive_date': inactive_date,
            'inactive_reason': inactive_reason,
            'bhs_pk': bhs_pk,
        }
        member, created = self.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
        return member, created


class UserManager(BaseUserManager):

    def update_or_create_from_person(self, person, **kwargs):
        if not person.email:
            raise ValidationError("Person must have email")
        created = False
        try:
            user = self.get(person=person)
        except self.model.DoesNotExist:
            created = True
            user = self.create_user(
                email=person.email,
                name=person.nomen,
                status=person.status,
            )
            person.user = user
            person.save()
            return user, created
        user.email = person.email
        user.name = person.nomen
        user.status = person.status
        return user, created

    def update_accounts(self, cursor=None, *args, **kwargs):
        # Get Base
        users = self.filter(
            status=self.model.STATUS.active,
            person__officers__isnull=False,  # for time being, only sync officers
        )
        if cursor:
            users = users.filter(
                modified__gt=cursor,
            )
        # Return as objects
        for user in users:
            update_or_create_account_from_user.delay(user)
        return users.count()

    def delete_orphans(self, *args, **kwargs):
        accounts = get_accounts()
        users = list(self.filter(
            account_id__isnull=False
        ).values_list('account_id', flat=True))
        for account in accounts:
            if account['account_id'] not in users:
                delete_account(account['account_id'])
        return

    def create_user(self, email, **kwargs):
        user = self.model(
            email=email,
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
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
