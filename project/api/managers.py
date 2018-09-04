# Standard Libary
import logging
import django_rq
import json
import uuid

# Django
from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import Manager
from django.db.models import F
from django.db.models import CharField
from django.db.models import Value
from django.forms.models import model_to_dict
from django.utils.timezone import now, localdate
from api.tasks import get_accounts
from api.tasks import create_account
from api.tasks import delete_account
from django.db.models.functions import Concat
from django.core.serializers.json import DjangoJSONEncoder
from dictdiffer import diff
from algoliasearch_django.decorators import disable_auto_indexing

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
            F('age').asc(nulls_first=True), # Null, Senior, Youth
            'gender', #Male, mixed
            'level', #Championship, qualifier
            'size', # Plateau v1
            'scope', # plateau
            'name', # alpha
        )
        i = 0
        for award in awards:
            i += 1
            award.tree_sort = i
            award.save()
        return


class GroupManager(Manager):
    def update_or_create_from_structure(self, structure):
        # Clean
        mc_pk = str(structure.id)
        raw_name = structure.name
        preferred_name = structure.preferred_name
        chorus_name = structure.chorus_name
        status = structure.status.name
        kind = structure.kind
        start_date = structure.established_date
        email = structure.email
        phone = structure.phone
        website = structure.website
        facebook = structure.facebook
        twitter = structure.twitter
        bhs_id = structure.bhs_id
        try:
            parent = str(structure.parent.id)
        except AttributeError:
            parent = None
        code = structure.chapter_code

        # Transform as needed
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
        mem_status = getattr(self.model.MEM_STATUS, status.replace("-", "_"))
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
            'mc_pk': mc_pk,
            'name': name,
            'status': status,
            'kind': kind,
            'start_date': start_date,
            'email': email,
            'phone': phone,
            'website': website,
            'facebook': facebook,
            'twitter': twitter,
            'code': code,
            'bhs_id': bhs_id,
            'mem_status': mem_status,
        }

        # Get or Create
        group, created = self.get_or_create(
            kind=kind,
            bhs_id=bhs_id,
        )

        if created:
            description = "Initial"
            # Update Values
            for key, value in defaults.items():
                setattr(group, key, value)
            # Set parent on create only
            if kind == self.model.KIND.chorus:
                kind = self.model.KIND.chapter
                name = raw_name.strip() if raw_name else 'UNKNOWN'
                parent, make = self.get_or_create(
                    name=name,
                    code=code,
                    bhs_id=bhs_id,
                    kind=kind,
                )
            else:
                if parent:
                    parent = self.get(mc_pk=parent)
            group.parent = parent
            # Do not transition groups in distdivs without divs
            divs = [
                'MAD',
                'FWD',
                'SWD',
                'LOL',
                'NED',
                'SWD',
            ]
            if parent.code in divs:
                group.save()
                return group, created
        else:
            # set prior values
            pre = model_to_dict(
                group,
                fields=[
                    'mc_pk',
                    'name',
                    'status',
                    'kind',
                    'start_date',
                    'email',
                    'phone',
                    'website',
                    'facebook',
                    'twitter',
                    'code',
                    'bhs_id',
                    'mem_status',
                ],
            )
            # update the group to new values
            for key, value in defaults.items():
                setattr(group, key, value)

            post = model_to_dict(
                group,
                fields=[
                    'mc_pk',
                    'name',
                    'status',
                    'kind',
                    'start_date',
                    'email',
                    'phone',
                    'website',
                    'facebook',
                    'twitter',
                    'code',
                    'bhs_id',
                    'mem_status',
                ],
            )
            result = list(diff(pre, post))
            if result:
                description = str(result)
            else:
                return group, created

        # Transition as appropriate
        if status == self.model.STATUS.active:
            group.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            group.deactivate(
                description=description,
            )
        elif status == self.model.STATUS.aic:
            pass
        else:
            raise ValueError('Unknown status')

        # Finally, save the record
        group.save()
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
            for grandchild in child.children.filter(
                kind=self.model.KIND.division,
            ).order_by('kind', 'name'):
                i += 1
                grandchild.tree_sort = i
                with disable_auto_indexing(model=self.model):
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

class MemberManager(Manager):
    def update_or_create_from_join(self, join):
        # Clean
        mc_pk = str(join.id)
        structure = str(join.structure.id)
        human = str(join.subscription.human.id)
        start_date = join.established_date
        end_date = join.inactive_date
        part = join.vocal_part
        # inactive_date = join.inactive_date
        # inactive_reason = join.inactive_reason
        # sub_status = join.subscription.status
        # mem_code = join.membership.code
        # mem_status = join.membership.status.name

        # Ignore rows without approval flow
        if not join.paid:
            return

        # Set status
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

        # inactive_reason = getattr(
        #     self.model.INACTIVE_REASON,
        #     inactive_reason.strip().replace("-", "_").replace(" ", "") if inactive_reason else '',
        #     None,
        # )

        # mem_code = getattr(
        #     self.model.MEM_CODE,
        #     mem_code if mem_code else '',
        #     None,
        # )

        # mem_status = getattr(
        #     self.model.MEM_STATUS,
        #     mem_status.strip().replace("-", "_") if mem_status else '',
        #     None,
        # )

        # Get the related fields
        Group = apps.get_model('api.group')
        group = Group.objects.get(
            mc_pk=structure,
        )
        Person = apps.get_model('api.person')
        try:
            person = Person.objects.get(
                mc_pk=human,
            )
        except Person.DoesNotExist:
            Human = apps.get_model('bhs.human')
            human = Human.objects.get(id=human)
            person, created = Person.objects.update_or_create_from_human(human)

        defaults = {
            'mc_pk': mc_pk,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
            'part': part,
        }

        # get or create
        member, created = self.get_or_create(
            person=person,
            group=group,
        )

        if created:
            description = "Initial"
            # update the group to new values
            for key, value in defaults.items():
                setattr(member, key, value)

        else:
            pre = model_to_dict(
                member,
                fields=[
                    'mc_pk',
                    'status',
                    'start_date',
                    'end_date',
                    'part',
                ],
            )
            # update the group to new values
            for key, value in defaults.items():
                setattr(member, key, value)
            post = model_to_dict(
                member,
                fields=[
                    'mc_pk',
                    'status',
                    'start_date',
                    'end_date',
                    'part',
                ],
            )
            result = list(diff(pre, post))
            if result:
                description = str(result)
            else:
                return member, created

        # Transition as appropriate
        if status == self.model.STATUS.active:
            member.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            member.deactivate(
                description=description,
            )
        else:
            raise ValueError('Unknown status')
        # Finally, save the record.
        member.save()
        return member, created


class OfficerManager(Manager):
    def update_or_create_from_role(self, role):
        # Clean
        mc_pk = str(role.id)
        office = role.name
        group = str(role.structure.id)
        person = str(role.human.id)
        start_date = role.start_date
        end_date = role.end_date

        # Set Variables
        today = now().date()
        if end_date:
            if end_date < today:
                status = self.model.STATUS.inactive
            else:
                status = self.model.STATUS.active
        else:
            status = self.model.STATUS.active

        # Get related fields
        Group = apps.get_model('api.group')
        group = Group.objects.get(mc_pk=group)
        Person = apps.get_model('api.person')
        person = Person.objects.get(mc_pk=person)
        Office = apps.get_model('api.office')
        office = Office.objects.get(name=office)

        defaults = {
            'mc_pk': mc_pk,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
        }

        # get or create
        officer, created = self.get_or_create(
            person=person,
            group=group,
            office=office,
        )

        if created:
            description = "Initial"
        else:
            pre = model_to_dict(
                officer,
                fields=[
                    'mc_pk',
                    'status',
                    'start_date',
                    'end_date',
                ],
            )
            # update the group to new values
            for key, value in defaults.items():
                setattr(officer, key, value)
            post = model_to_dict(
                officer,
                fields=[
                    'mc_pk',
                    'status',
                    'start_date',
                    'end_date',
                ],
            )
            result = list(diff(pre, post))
            if result:
                description = str(result)
            else:
                return officer, created

        # Transition as appropriate
        if status == self.model.STATUS.active:
            officer.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            officer.deactivate(
                description=description,
            )
        else:
            raise ValueError('Unknown status')
        # Finally, save the record.  Break link if an overwrite to MC
        officer.save()
        return officer, created


class PersonManager(Manager):
    def update_or_create_from_human(self, human):
        # Clean
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

        # Same logic regardless of inbound form
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

        # Status check?
        # if is_deceased:
        #     status = self.model.STATUS.active
        # else:
        #     status = self.model.STATUS.inactive

        defaults = {
            'mc_pk': mc_pk,
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
        # Get or create
        try:
            person = self.get(
                mc_pk=mc_pk,
            )
            created = False
        except self.model.DoesNotExist:
            try:
                person = self.create(
                    **defaults,
                )
            except IntegrityError as e:
                # Need to delete old offending record
                if "api_person_bhs_id_key" in str(e.args):
                    old = self.get(
                        bhs_id=bhs_id,
                    )
                    old.delete()
                    person = self.create(
                        **defaults,
                    )
                else:
                    defaults['mc_pk'] = mc_pk
                    defaults.pop('bhs_id', None)
                    try:
                        person = self.create(
                            **defaults,
                        )
                    except IntegrityError:
                        defaults['mc_pk'] = mc_pk
                        defaults['bhs_id'] = bhs_id
                        defaults.pop('email', None)
                        person = self.create(
                            **defaults,
                        )
            created = True

        if created:
            description = "Initial"
            # Update Values
            for key, value in defaults.items():
                setattr(person, key, value)
        else:
            # set prior values
            pre = model_to_dict(
                person,
                fields=[
                    'mc_pk',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'nick_name',
                    'email',
                    'birth_date',
                    'phone',
                    'cell_phone',
                    'work_phone',
                    'bhs_id',
                    'gender',
                    'part',
                    'is_deceased',
                ],
            )
            for key, value in defaults.items():
                setattr(person, key, value)

            post = model_to_dict(
                person,
                fields=[
                    'mc_pk',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'nick_name',
                    'email',
                    'birth_date',
                    'phone',
                    'cell_phone',
                    'work_phone',
                    'bhs_id',
                    'gender',
                    'part',
                    'is_deceased',
                ],
            )
            result = list(diff(pre, post))
            if result:
                description = str(result)
            else:
                return person, created

        # Transition as appropriate
        if person.status == person.STATUS.active:
            person.activate(
                description=description,
            )
        elif person.status == person.STATUS.inactive:
            person.deactivate(
                description=description,
            )
        else:
            pass
        # Finally, save the record
        person.save()
        return person, created


class UserManager(BaseUserManager):
    def update_or_create_from_subscription(self, subscription):
        # Clean
        mc_pk = str(subscription.id)
        human = subscription.human
        current_through = subscription.current_through

        status = getattr(
            self.model.STATUS,
            subscription.status,
            self.model.STATUS.inactive,
        )

        Person = apps.get_model('api.person')
        person, created = Person.objects.update_or_create_from_human(human)
        name = person.nomen
        email = person.email
        if not email:
            return
        defaults = {
            'mc_pk': mc_pk,
            'status': status,
            'name': name,
            'email': email,
            'current_through': current_through,
            'person': person,
        }

        # Get or create
        try:
            user = self.get(
                person=person,
            )
            created = False
        except self.model.DoesNotExist:
            try:
                user = self.create_user(
                    **defaults,
                )
            except IntegrityError as e:
                # Need to delete old offending record
                if "api_user_mc_pk_key" in str(e.args):
                    old = self.get(
                        mc_pk=mc_pk,
                    )
                    old.delete()
                    user = self.create_user(
                        **defaults,
                    )
                else:
                    raise(e)
        created = True

        if created:
            description = "Initial"
        else:
            pre = model_to_dict(
                user,
                fields=[
                    'mc_pk',
                    'status',
                    'name',
                    'email',
                    'current_through',
                    'person',
                ],
            )
            # update the person to new values
            for key, value in defaults.items():
                setattr(user, key, value)
            post = model_to_dict(
                user,
                fields=[
                    'mc_pk',
                    'status',
                    'name',
                    'email',
                    'current_through',
                    'person',
                ],
            )
            result = list(diff(pre, post))
            if result:
                description = str(result)
            else:
                return user, created

        if status == self.model.STATUS.active:
            user.activate(
                description=description,
            )
        elif status == self.model.STATUS.inactive:
            user.deactivate(
                description=description,
            )
        else:
            raise ValueError('Unknown status')
        user.save()
        return user, created


    def delete_orphans(self):
        auth0 = get_auth0()
        queue = django_rq.get_queue('low')
        accounts = get_accounts()
        users = list(self.filter(
            username__startswith='auth0|',
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

    def create_user(self, username=None, **kwargs):
        pk = uuid.uuid4()
        if not username:
            username = "orphan|{0}".format(str(pk))
        user = self.model(
            id=pk,
            username=username,
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
