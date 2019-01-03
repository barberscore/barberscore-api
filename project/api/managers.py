
# Standard Library
import json
import logging
import uuid
import maya

# Third-Party
import django_rq
from algoliasearch_django.decorators import disable_auto_indexing
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import CharField
from django.db.models import F
from django.db.models import Manager
from django.db.models import Value
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.utils.timezone import localdate
from django.utils.timezone import now

# First-Party
from api.tasks import get_accounts
from api.tasks import get_auth0

log = logging.getLogger(__name__)

validate_url = URLValidator()

validate_twitter = RegexValidator(
    regex=r'@([A-Za-z0-9_]+)',
    message="""
        Must be a single Twitter handle
        in the form `@twitter_handle`.
    """,
)


class AwardManager(Manager):
    def sort_tree(self):
        self.all().update(tree_sort=None)
        awards = self.order_by(
            '-status',  # Actives first
            'group__tree_sort',  # Basic BHS Hierarchy
            '-kind', # Quartet, Chorus
            'gender', #Male, mixed
            F('age').asc(nulls_first=True), # Null, Senior, Youth
            'level', #Championship, qualifier
            'name', # alpha
        )
        i = 0
        for award in awards:
            i += 1
            award.tree_sort = i
            award.save()
        return


class ChartManager(Manager):
    def get_report(self):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'PK',
            'Title',
            'Arrangers',
            'Composers',
            'Lyricists',
            'Holders',
            'Status',
        ]
        ws.append(fieldnames)
        charts = self.order_by('title', 'arrangers')
        for chart in charts:
            pk = str(chart.pk)
            title = chart.title
            arrangers = chart.arrangers
            composers = chart.composers
            lyricists = chart.lyricists
            holders = chart.holders
            status = chart.get_status_display()
            row = [
                pk,
                title,
                arrangers,
                composers,
                lyricists,
                holders,
                status,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content


class GroupManager(Manager):
    def update_or_create_from_structure(self, structure):
        # Extract
        mc_pk = str(structure.id)
        raw_name = structure.name
        preferred_name = structure.preferred_name
        chorus_name = structure.chorus_name
        status = structure.status.name
        kind = structure.kind
        gender = structure.sex
        start_date = structure.established_date
        email = structure.email
        phone = structure.phone
        website = structure.website
        facebook = structure.facebook
        twitter = structure.twitter
        bhs_id = structure.bhs_id
        try:
            parent = self.get(mc_pk=structure.parent.id)
        except AttributeError:
            parent = None
        except self.model.DoesNotExist:
            parent = None
        code = structure.chapter_code

        # Transform
        name = raw_name.strip() if raw_name else ''
        preferred_name = "{0} (NAME APPROVAL PENDING)".format(preferred_name) if preferred_name else ''
        chorus_name = chorus_name.strip() if chorus_name else ''
        kind = getattr(
            self.model.KIND,
            kind.replace(
                'chapter', 'chorus'
            ).replace(
                'group', 'noncomp'
            ).replace(
                'organization', 'international'
            )
        )
        gender = getattr(
            self.model.GENDER,
            gender.replace(
                'men', 'male'
            ).replace(
                'women', 'female'
            )
        )
        if email:
            email = email.strip().lower()
            try:
                validate_email(email)
            except ValidationError:
                email = None
        else:
            email = None
        phone = phone.strip()
        website = website.strip()
        facebook = facebook.strip()
        twitter = twitter.strip()
        status = getattr(self.model.STATUS, status, self.model.STATUS.inactive)
        code = code.strip() if code else ''

        # Construct the group name
        if kind == self.model.KIND.quartet:
            # If the name has not been assigned, use preferred. Otherwise, call unknown.
            if not name:
                name = preferred_name if preferred_name else 'UNKNOWN'
        elif kind == self.model.KIND.chorus:
            name = chorus_name if chorus_name else 'UNKNOWN'
        else:
            name = name if name else 'UNKNOWN'

        # Clean website
        try:
            validate_url(website)
        except ValidationError:
            website = ""

        # Clean facebook
        try:
            validate_url(facebook)
        except ValidationError:
            facebook = ""

        # Clean twitter
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
        if str(bhs_id) in self.model.AIC:
            status = getattr(self.model.STATUS, 'aic')
            name = self.model.AIC[str(bhs_id)]
        defaults = {
            'name': name,
            'status': status,
            'kind': kind,
            'gender': gender,
            'start_date': start_date,
            'email': email,
            'phone': phone,
            'website': website,
            'facebook': facebook,
            'twitter': twitter,
            'parent': parent,
            'code': code,
            'bhs_id': bhs_id,
        }

        # Update or Create
        try:
            group, created = self.update_or_create(
                mc_pk=mc_pk,
                defaults=defaults,
            )
        except IntegrityError as e:
            # Need to delete old offending record
            if "api_group_bhs_id_kind" in str(e.args):
                old = self.get(
                    bhs_id=bhs_id,
                )
                old.delete()
                group, created = self.update_or_create(
                    mc_pk=mc_pk,
                    defaults=defaults,
                )
            else:
                raise e
        return group, created

    def sort_tree(self):
        self.all().update(tree_sort=None)
        root = self.get(kind=self.model.KIND.international)
        i = 1
        root.tree_sort = i
        with disable_auto_indexing(model=self.model):
            root.save()
        for child in root.children.order_by('kind', 'code', 'name'):
            i += 1
            child.tree_sort = i
            with disable_auto_indexing(model=self.model):
                child.save()
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
            with disable_auto_indexing(model=self.model):
                org.save()
        return

    def denormalize(self, cursor=None):
        groups = self.filter(status=self.model.STATUS.active)
        if cursor:
            groups = groups.filter(
                modified__gte=cursor,
            )
        for group in groups:
            group.denormalize()
            with disable_auto_indexing(model=self.model):
                group.save()
        return

    def update_seniors(self):
        quartets = self.filter(
            kind=self.model.KIND.quartet,
            status__gt=0,
            mc_pk__isnull=False,
        )

        for quartet in quartets:
            prior = quartet.is_senior
            is_senior = quartet.get_is_senior()
            if prior != is_senior:
                quartet.is_senior = is_senior
                with disable_auto_indexing(model=self.model):
                    quartet.save()
        return

    def get_quartets(self):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'PK',
            'Name',
            'Kind',
            'Organization',
            'District',
            'Chapter',
            'Senior?',
            'BHS ID',
            'Code',
            'Status',
        ]
        ws.append(fieldnames)
        groups = self.filter(
            status=self.model.STATUS.active,
            kind=self.model.KIND.quartet,
        ).order_by('name')
        for group in groups:
            pk = str(group.pk)
            name = group.name
            kind = group.get_kind_display()
            organization = group.international
            district = group.district
            chapter = group.chapter
            is_senior = group.is_senior
            bhs_id = group.bhs_id
            code = group.code
            status = group.get_status_display()
            row = [
                pk,
                name,
                kind,
                organization,
                district,
                chapter,
                is_senior,
                bhs_id,
                code,
                status,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content


class MemberManager(Manager):
    def update_or_create_from_join(self, join):
        # Ignore rows without approval flow
        if not join.paid:
            return

        # Extract
        mc_pk = str(join.id)
        structure = str(join.structure.id)
        human = str(join.subscription.human.id)
        start_date = join.established_date
        end_date = join.subscription.current_through
        part = join.vocal_part

        # Transform
        if not end_date:
            status = self.model.STATUS.active
        elif end_date > localdate():
            status = self.model.STATUS.active
        else:
            status = self.model.STATUS.inactive
        part = getattr(
            self.model.PART,
            part.strip().lower() if part else '',
            None,
        )

        # Build dictionary
        defaults = {
            'mc_pk': mc_pk,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
            'part': part,
        }

        # Get the related fields
        Group = apps.get_model('api.group')
        try:
            group = Group.objects.get(
                mc_pk=structure,
            )
        except Group.DoesNotExist:
            Structure = apps.get_model('bhs.structure')
            structure = Structure.objects.get(id=structure)
            group, created = Group.objects.update_or_create_from_structure(structure)

        Person = apps.get_model('api.person')
        try:
            person = Person.objects.get(
                mc_pk=human,
            )
        except Person.DoesNotExist:
            Human = apps.get_model('bhs.human')
            human = Human.objects.get(id=human)
            person, created = Person.objects.update_or_create_from_human(human)

        # get or create
        member, created = self.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
        return member, created


class OfficerManager(Manager):
    def update_or_create_from_role(self, role):
        # Extract
        mc_pk = str(role.id)
        office = role.name
        group = str(role.structure.id)
        person = str(role.human.id)
        start_date = role.start_date
        end_date = role.end_date

        # Transform
        today = now().date()
        if end_date:
            if end_date < today:
                status = self.model.STATUS.inactive
            else:
                status = self.model.STATUS.active
        else:
            status = self.model.STATUS.active

        # Load
        defaults = {
            'mc_pk': mc_pk,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
        }

        # Get related fields
        Group = apps.get_model('api.group')
        group = Group.objects.get(mc_pk=group)
        Person = apps.get_model('api.person')
        person = Person.objects.get(mc_pk=person)
        Office = apps.get_model('api.office')
        office = Office.objects.get(name=office)

        # get or create
        officer, created = self.update_or_create(
            person=person,
            group=group,
            office=office,
            defaults=defaults,
        )
        return officer, created


class PersonManager(Manager):
    def update_or_create_from_human(self, human):
        # Extract
        mc_pk = str(human.id)
        first_name = human.first_name
        middle_name = human.middle_name
        last_name = human.last_name
        nick_name = human.nick_name
        email = human.email
        birth_date = human.birth_date
        phone = human.phone
        cell_phone = human.cell_phone
        work_phone = human.work_phone
        bhs_id = human.bhs_id
        gender = human.sex
        part = human.primary_voice_part
        is_deceased = human.is_deceased

        # Transform
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
            email = email.strip().lower()
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

        is_deceased = bool(is_deceased)

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
            'is_deceased': is_deceased,
        }
        # Update or create
        person, created = self.update_or_create(
            mc_pk=mc_pk,
            defaults=defaults,
        )
        return person, created


class UserManager(BaseUserManager):
    def delete_orphans(self):
        auth0 = get_auth0()
        queue = django_rq.get_queue('low')
        accounts = get_accounts()
        users = list(self.filter(
            is_staff=False,
        ).values_list('username', flat=True))
        i = 0
        for account in accounts:
            if account[0] not in users:
                i += 1
                queue.enqueue(
                    auth0.users.delete,
                    account[0],
                )
        return i

    def create_user(self, person, **kwargs):
        pk = uuid.uuid4()
        auth0 = get_auth0()
        password = self.make_random_password()
        payload = {
            'connection': 'Default',
            'email': person.email,
            'email_verified': True,
            'password': password,
            'app_metadata': {
                'name': person.common_name,
            }
        }
        account = auth0.users.create(payload)
        username = account['user_id']
        user = self.model(
            id=pk,
            username=username,
            person=person,
            **kwargs
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(
            username=username,
            status=self.model.STATUS.active,
            is_staff=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
