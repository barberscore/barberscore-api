from datetime import date

# Third-Party
import django_rq
from django_fsm_log.models import StateLog

# Django
from django.apps import apps
from django.db.models import Manager
from django.db.models import Q
from django.db.models import F
from django.db.models import Min
from django.db.models import Max
from django.db.models import When
from django.db.models import Subquery
from django.db.models import OuterRef
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import DateField
from django.db.models import Case

from .tasks import get_accounts


class HumanManager(Manager):
    def export_values(self, cursor=None):
        hs = self.filter(
            Q(merged_id="") | Q(merged_id=None),
            Q(deleted_id="") | Q(deleted_id=None),
        )
        if cursor:
            hs = hs.filter(
                modified__gte=cursor,
            )
        return list(hs.values(
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'email',
            'birth_date',
            'home_phone',
            'cell_phone',
            'work_phone',
            'bhs_id',
            'gender',
            'part',
            'mon',
            'is_deceased',
            'is_honorary',
            'is_suspended',
            'is_expelled',
        ))

    def delete_orphans(self):
        # Get base
        humans = list(self.values_list('id', flat=True))
        # Delete Orphans
        Person = apps.get_model('api.person')
        orphans = Person.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=humans,
        )
        t = orphans.count()
        orphans.delete()
        return t


    def get_account_orphans(self):
        # Get humans
        humans = list(self.values_list('id', flat=True))
        # Get accounts
        accounts = get_accounts()
        mc_pks = [x['app_metadata']['mc_pk'] for x in accounts]
        # Get orphans
        orphans = [{'id': item} for item in mc_pks if item not in humans]
        return orphans


    def get_account_adoptions(self):
        # Get accounts
        accounts = get_accounts()
        mc_pks = [x['app_metadata']['mc_pk'] for x in accounts]
        # Get current
        human_values = list(self.values(
            'id',
            'first_name',
            'last_name',
            'nick_name',
            'email',
            'bhs_id',
        ))
        # Rebuild list for verified emails only.
        # Can skip this part if we trust MC data (which we don't currently)
        humans = [x for x in human_values if x['email']]
        # Get adoptions
        adoptions = [item for item in humans if item['id'] not in mc_pks]
        return adoptions


class StructureManager(Manager):
    def export_values(self, cursor=None):
        output = []
        types = [
            'organization',
            'district',
            'group',
            'chapter',
            'chorus',
            'quartet',
        ]
        for t in types:
            ss = self.filter(
                Q(kind=t),
                Q(deleted_id="") | Q(deleted_id=None),
            )
            if cursor:
                ss = ss.filter(
                    modified__gte=cursor,
                )
            output.extend(
                list(ss.values(
                    'id',
                    'name',
                    'kind',
                    'gender',
                    'division',
                    'bhs_id',
                    'chapter_code',
                    'website',
                    'email',
                    'phone',
                    'fax',
                    'facebook',
                    'twitter',
                    'youtube',
                    'pinterest',
                    'flickr',
                    'instagram',
                    'soundcloud',
                    'preferred_name',
                    'visitor_information',
                    'established_date',
                    'status_id',
                    'parent_id',
                ))
            )
        return output

    def delete_orphans(self):
        # Get base
        structures = list(self.values_list('id', flat=True))
        # Delete Orphans
        Group = apps.get_model('api.group')
        orphans = Group.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=structures,
        )
        t = orphans.count()
        orphans.delete()
        return t


class JoinManager(Manager):
    def export_values(self, cursor=None):
        Structure = apps.get_model('bhs.structure')
        today = date.today()
        js = self.select_related(
            'structure',
            'membership',
            'subscription',
            'subscription__human',
        ).filter(
            Q(paid=True),
            Q(deleted__isnull=True),
            Q(membership__deleted_id="") | Q(membership__deleted_id=None),
            Q(subscription__deleted=None),
            Q(structure__deleted_id="") | Q(structure__deleted_id=None),
            Q(subscription__human__merged_id="") | Q(subscription__human__merged_id=None),
            Q(subscription__human__deleted_id="") | Q(subscription__human__deleted_id=None),
        )
        if cursor:
            js = js.filter(
                Q(modified__gte=cursor) |
                Q(membership__modified__gte=cursor) |
                Q(subscription__modified__gte=cursor)
            )
        js = js.values(
            'structure__id',
            'subscription__human__id',
        )
        js = js.annotate(
            id=Max('id'),
            vocal_part=Subquery(
                self.filter(
                    structure__id=OuterRef('structure__id'),
                    subscription__human__id=OuterRef('subscription__human__id'),
                ).order_by(
                    '-modified',
                ).values('part')[:1],
                output_field=CharField()
            ),
            inactivist_date=Subquery(
                self.filter(
                    structure__id=OuterRef('structure__id'),
                    subscription__human__id=OuterRef('subscription__human__id'),
                ).order_by(
                    F('inactive_date').desc(nulls_first=True)
                ).values('inactive_date')[:1],
                output_field=DateField()
            ),
            currentest_date=Subquery(
                self.filter(
                    structure__id=OuterRef('structure__id'),
                    subscription__human__id=OuterRef('subscription__human__id'),
                ).order_by(
                    F('subscription__current_through').desc(nulls_first=True)
                ).values('subscription__current_through')[:1],
                output_field=DateField()
            ),
            startest_date=Min('established_date'),
            endest_date=Case(
                When(
                    Q(
                        structure__kind__in=[
                            Structure.KIND.chorus,
                            Structure.KIND.chapter,
                        ],
                    ),
                    then=F('inactivist_date'),
                ),
                default=F('currentest_date'),
                output_field=DateField(),
            ),
            status=Case(
                When(endest_date__isnull=True, then=10),
                When(endest_date__gte=today, then=10),
                default=-10,
                output_field=IntegerField(),
            ),
        ).values(
            'structure__id',
            'subscription__human__id',
            'id',
            'vocal_part',
            'startest_date',
            'endest_date',
            'status',
        )
        return list(js)

    def delete_orphans(self):
        # Get base
        joins = list(self.values_list('id', flat=True))
        # Delete Orphans
        Member = apps.get_model('api.member')
        orphans = Member.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=joins,
        )
        t = orphans.count()
        orphans.delete()
        return t


class RoleManager(Manager):
    def export_values(self, cursor=None):
        today = date.today()
        rs = self.filter(
            Q(structure__deleted_id="") | Q(structure__deleted_id=None),
            Q(human__merged_id="") | Q(human__merged_id=None),
            Q(human__deleted_id="") | Q(human__deleted_id=None),
        )
        if cursor:
            rs = rs.filter(
                modified__gte=cursor,
            )
        return list(rs.values(
            'name',
            'human_id',
            'structure_id',
        ).annotate(
            id=Max('id'),
            startest_date=Min('start_date'),
            endest_date=Max('end_date'),
            status=Case(
                When(endest_date=None, then=10),
                When(endest_date__gte=today, then=10),
                default=-10,
                output_field=IntegerField(),
            ),
        ))

    def delete_orphans(self):
        # Get base
        roles = list(self.values_list('id', flat=True))
        # Delete Orphans
        Officer = apps.get_model('api.officer')
        orphans = Officer.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=roles,
        )
        t = orphans.count()
        orphans.delete()
        return t


class PersonManager(Manager):
    def export_orphans(self, cursor=None):
        ps = self.filter(
            email__isnull=True,
            user__isnull=False,
        )
        if cursor:
            ps = ps.filter(
                modified__gte=cursor,
            )
        return ps

    def export_adoptions(self, cursor=None):
        ps = self.filter(
            email__isnull=False,
            user__isnull=True,
        )
        if cursor:
            ps = ps.filter(
                modified__gte=cursor,
            )
        return ps

    def update_or_create_from_human(self, human):
        # Extract
        if isinstance(human, dict):
            mc_pk = human['id']
            first_name = human['first_name']
            middle_name = human['middle_name']
            last_name = human['last_name']
            nick_name = human['nick_name']
            email = human['email']
            birth_date = human['birth_date']
            home_phone = human['home_phone']
            cell_phone = human['cell_phone']
            work_phone = human['work_phone']
            bhs_id = human['bhs_id']
            gender = human['gender']
            part = human['part']
            mon = human['mon']
            is_deceased = human['is_deceased']
            is_honorary = human['is_honorary']
            is_suspended = human['is_suspended']
            is_expelled = human['is_expelled']
        else:
            mc_pk = str(human.id)
            first_name = human.first_name
            middle_name = human.middle_name
            last_name = human.last_name
            nick_name = human.nick_name
            email = human.email
            birth_date = human.birth_date
            home_phone = human.home_phone
            cell_phone = human.cell_phone
            work_phone = human.work_phone
            bhs_id = human.bhs_id
            gender = human.gender
            part = human.part
            mon = human.mon
            is_deceased = human.is_deceased
            is_honorary = human.is_honorary
            is_suspended = human.is_suspended
            is_expelled = human.is_expelled

        # Transform
        inactive = any([
            is_deceased,
            is_honorary,
            is_suspended,
            is_expelled,
        ])
        if inactive:
            status = self.model.STATUS.inactive
        else:
            status = self.model.STATUS.active

        prefix = first_name.rpartition('Dr.')[1].strip()
        first_name = first_name.rpartition('Dr.')[2].strip()
        last_name = last_name.partition('II')[0].strip()
        suffix = last_name.partition('II')[1].strip()
        last_name = last_name.partition('III')[0].strip()
        suffix = last_name.partition('III')[1].strip()
        last_name = last_name.partition('DDS')[0].strip()
        suffix = last_name.partition('DDS')[1].strip()
        last_name = last_name.partition('Sr')[0].strip()
        suffix = last_name.partition('Sr')[1].strip()
        last_name = last_name.partition('Jr')[0].strip()
        suffix = last_name.partition('Jr')[1].strip()
        last_name = last_name.partition('M.D.')[0].strip()
        suffix = last_name.partition('M.D.')[1].strip()
        if nick_name == first_name:
            nick_name = ""
        if gender:
            gender = getattr(self.model.GENDER, gender, None)
        else:
            gender = None
        if part:
            part = getattr(self.model.PART, part, None)
        else:
            part = None

        is_deceased = bool(is_deceased)


        defaults = {
            'status': status,
            'prefix': prefix,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'suffix': suffix,
            'nick_name': nick_name,
            'email': email,
            'birth_date': birth_date,
            'home_phone': home_phone,
            'cell_phone': cell_phone,
            'work_phone': work_phone,
            'bhs_id': bhs_id,
            'gender': gender,
            'part': part,
            'is_deceased': is_deceased,
            'mon': mon,
        }
        # Update or create
        person, created = self.update_or_create(
            mc_pk=mc_pk,
            defaults=defaults,
        )
        return person, created

    def delete_orphans(self, humans):
        # Delete Orphans
        orphans = self.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=humans,
        )
        t = orphans.count()
        orphans.delete()
        return t

