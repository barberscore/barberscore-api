

# Third-Party
import django_rq

# Django
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

# First-Party
from bhs.managers import HumanManager
from bhs.managers import JoinManager
from bhs.managers import RoleManager
from bhs.managers import StructureManager
# from bhs.managers import SubscriptionManager
from model_utils import Choices

from bhs.fields import McEmailField
from bhs.fields import McVoicePartField
from bhs.fields import McGenderField


class Human(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    first_name = models.CharField(
        max_length=255,
        editable=False,
    )
    middle_name = models.CharField(
        max_length=255,
        editable=False,
        db_column='middle_initial',
    )
    last_name = models.CharField(
        max_length=255,
        editable=False,
    )
    nick_name = models.CharField(
        max_length=255,
        editable=False,
        db_column='preferred_name',
    )
    email = McEmailField(
        max_length=255,
        unique=True,
        editable=False,
        db_column='username',
    )
    birth_date = models.DateField(
        editable=False,
        null=True,
        db_column='birthday'
    )
    is_deceased = models.BooleanField(
        editable=False,
    )
    phone = models.CharField(
        max_length=255,
        editable=False,
    )
    cell_phone = models.CharField(
        max_length=255,
        editable=False,
    )
    work_phone = models.CharField(
        max_length=255,
        editable=False,
    )
    bhs_id = models.IntegerField(
        editable=False,
        unique=True,
        null=False,
        db_column='legacy_id',
    )
    SEX = Choices(
        ('male', 'Male'),
        ('female', 'Female'),
    )
    sex = models.CharField(
        max_length=255,
        editable=False,
        choices=SEX,
    )
    PART = Choices(
        ('tenor', 'Tenor'),
        ('lead', 'Lead'),
        ('baritone', 'Baritone'),
        ('bass', 'Bass'),
    )
    primary_voice_part = McVoicePartField(
        max_length=255,
        editable=False,
        choices=PART,
    )

    created = models.DateTimeField(
        db_column='created',
        null=False,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        null=True,
        editable=False,
    )

    deleted = models.DateTimeField(
        db_column='deleted',
        null=True,
        editable=False,
    )

    objects = HumanManager()

    # Properties
    @cached_property
    def full_name(self):
        if self.first_name:
            first_name = self.first_name.strip()
        else:
            first_name = None
        if self.middle_name:
            middle_name = self.middle_name.strip()
        else:
            middle_name = None
        if self.last_name:
            last_name = self.last_name.strip()
        else:
            last_name = None
        if self.nick_name:
            format_nick = "({0})".format(
                self.nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
            )
        else:
            format_nick = None
        full_name = " ".join(
            filter(
                None, [
                    first_name,
                    middle_name,
                    last_name,
                    format_nick,
                ]
            )
        )
        return full_name

    # Internals
    def __str__(self):
        return "{0} [{1}]".format(
            self.full_name,
            self.bhs_id,
        )

    def update_bs(self):
        Person = apps.get_model('api.person')
        Member = apps.get_model('api.member')
        Officer = apps.get_model('api.officer')
        Person.objects.update_or_create_from_human(self)
        joins = self.get_joins()
        for join in joins:
            Member.objects.update_or_create_from_join(join)
        roles = self.get_roles()
        for role in roles:
            Officer.objects.update_or_create_from_role(role)
        return

    def get_joins(self):
        Join = apps.get_model('bhs.join')
        structures = self.subscriptions.prefetch_related(
            'joins__structure',
        ).values_list(
            'joins__structure',
            flat=True,
        ).distinct()
        joins = []
        for structure in structures:
            try:
                join = Join.objects.select_related(
                    'subscription__human',
                    'structure',
                ).filter(
                    paid=True,
                    deleted__isnull=True,
                    subscription__human=self,
                    structure__id=structure,
                ).latest(
                    'modified',
                    '-inactive_date',
                )
            except Join.DoesNotExist:
                continue
            joins.append(join)
        return joins

    def get_roles(self):
        pairs = self.roles.select_related(
            'structure',
        ).values_list(
            'structure',
            'name',
        ).distinct()
        roles = []
        for structure, name in pairs:
            role = self.roles.select_related(
                'structure',
            ).filter(
                structure__id=structure,
                name=name,
            ).latest(
                'modified',
                '-end_date',
            )
            roles.append(role)
        return roles

    class Meta:
        managed=False
        db_table = 'vwMembers'


class Structure(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    KIND = Choices(
        ('organization', 'Organization'),
        ('district', 'District'),
        ('group', 'Group'),
        ('chapter', 'Chapter'),
        ('chorus', 'Chorus'),
        ('quartet', 'Quartet'),
    )
    kind = models.CharField(
        max_length=255,
        editable=False,
        choices=KIND,
        db_column='object_type',
    )
    GENDER = Choices(
        ('men', 'Male'),
        ('women', 'Female'),
        ('mixed', 'Mixed'),
    )
    gender = models.CharField(
        max_length=255,
        editable=False,
        choices=GENDER,
        db_column='category'
    )
    bhs_id = models.IntegerField(
        editable=False,
        unique=True,
        null=False,
        db_column='legacy_id',
    )
    chapter_code = models.CharField(
        max_length=255,
        editable=False,
        db_column='legacy_code',
    )
    chorus_name = models.CharField(
        max_length=255,
        editable=False,
    )
    preferred_name = models.CharField(
        max_length=255,
        editable=False,
    )
    phone = models.CharField(
        max_length=255,
        editable=False,
    )
    email = models.CharField(
        max_length=255,
        editable=False,
    )
    website = models.CharField(
        max_length=255,
        editable=False,
    )
    facebook = models.CharField(
        max_length=255,
        editable=False,
    )
    twitter = models.CharField(
        max_length=255,
        editable=False,
    )
    established_date = models.DateField(
        editable=False,
    )
    created = models.DateTimeField(
        db_column='created',
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        editable=False,
    )
    deleted = models.DateTimeField(
        db_column='deleted',
        null=True,
        editable=False,
    )

    # FKs
    status = models.ForeignKey(
        'Status',
        related_name='structures',
        editable=False,
        on_delete=models.CASCADE,
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_column='parent_id',
        on_delete=models.CASCADE,
    )

    objects = StructureManager()

    def __str__(self):
        if self.name:
            name = self.name.strip()
        else:
            name = 'UNKNOWN'
        return "{0} [{1}]".format(
            name,
            self.bhs_id,
        )


    def update_bs(self):
        Group = apps.get_model('api.group')
        Member = apps.get_model('api.member')
        Officer = apps.get_model('api.officer')
        Group.objects.update_or_create_from_structure(self)
        joins = self.get_joins()
        for join in joins:
            Member.objects.update_or_create_from_join(join)
        roles = self.get_roles()
        for role in roles:
            Officer.objects.update_or_create_from_role(role)
        return


    def get_joins(self):
        humans = self.joins.select_related(
            'subscription__human',
        ).values_list(
            'subscription__human',
            flat=True,
        ).distinct()
        joins = []
        for human in humans:
            try:
                join = self.joins.select_related(
                    'subscription',
                    'subscription__human',
                ).filter(
                    paid=True,
                    deleted__isnull=True,
                    subscription__human__id=human,
                ).latest(
                    'modified',
                    '-inactive_date',
                )
            except self.joins.model.DoesNotExist:
                continue
            joins.append(join)
        return joins

    def get_roles(self):
        pairs = self.roles.select_related(
            'human',
        ).values_list(
            'human',
            'name',
        ).distinct()
        roles = []
        for human, name in pairs:
            role = self.roles.select_related(
                'human',
            ).filter(
                human__id=human,
                name=name,
            ).latest(
                'modified',
                '-end_date',
            )
            roles.append(role)
        return roles

    class Meta:
        managed=False
        db_table = 'vwStructures'


class Status(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    # Internals

    def __str__(self):
        return str(self.name)

    class Meta:
        managed=False
        db_table = 'vwStatuses'
        verbose_name_plural = 'statuses'


class Membership(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )

    code = models.CharField(
        max_length=255,
        editable=False,
    )

    created = models.DateTimeField(
        db_column='created',
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='modified',
        editable=False,
    )
    deleted = models.DateTimeField(
        db_column='deleted',
        editable=False,
    )

    # FKs
    structure = models.ForeignKey(
        'Structure',
        related_name='memberships',
        editable=False,
        db_column='object_id',
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        'Status',
        related_name='memberships',
        editable=False,
        on_delete=models.CASCADE,
    )

    # Internals
    def __str__(self):
        return "{0} {1}".format(
            self.structure,
            self.code,
        )

    class Meta:
        managed=False
        db_table = 'vwMemberships'


class Subscription(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    current_through = models.DateField(
        db_column='valid_through',
        null=True,
        editable=False,
    )
    status = models.CharField(
        max_length=255,
        editable=False,
    )
    items_editable = models.BooleanField(
        editable=False,
    )
    created = models.DateTimeField(
        db_column='created',
        null=False,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        null=True,
        editable=False,
    )
    deleted = models.DateTimeField(
        db_column='deleted',
        null=True,
        editable=False,
    )

    # objects = SubscriptionManager()

    # FKs
    human = models.ForeignKey(
        'Human',
        related_name='subscriptions',
        editable=False,
        db_column='members_id',
        on_delete=models.CASCADE,
    )

    # Internals
    def __str__(self):
        return str(self.human)

    class Meta:
        managed = False
        db_table = 'vwSubscriptions'


class Role(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    abbv = models.CharField(
        max_length=255,
        editable=False,
    )
    officer_roles_id = models.CharField(
        max_length=255,
        editable=False,
    )
    start_date = models.DateField(
        null=True,
        editable=False,
    )
    end_date = models.DateField(
        null=True,
        editable=False,
    )
    # FKs
    human = models.ForeignKey(
        'Human',
        related_name='roles',
        editable=False,
        db_column='member_id',
        on_delete=models.CASCADE,
    )
    structure = models.ForeignKey(
        'Structure',
        related_name='roles',
        editable=False,
        db_column='object_id',
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(
        db_column='created',
        null=False,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        null=True,
        editable=False,
    )

    objects = RoleManager()

    # Internals
    def __str__(self):
        return "{0} {1} {2}".format(
            self.name,
            self.human,
            self.structure,
        )

    def clean(self):
        if self.name.partition(" ")[0].lower() != self.structure.kind:
            raise ValidationError({
                'name': 'Role name does not match structure type.',
            })


    class Meta:
        managed=False
        db_table = 'vwOfficers'


class Join(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    status = models.BooleanField(
        editable=False,
    )
    paid = models.BooleanField(
        editable=False,
    )
    PART = Choices(
        ('tenor', 'Tenor'),
        ('lead', 'Lead'),
        ('baritone', 'Baritone'),
        ('bass', 'Bass'),
    )
    vocal_part = McVoicePartField(
        max_length=255,
        editable=False,
        choices=PART,
    )
    established_date = models.DateField(
        db_column='created',
        null=False,
        editable=False,
    )
    inactive_date = models.DateField(
        db_column='inactive',
        null=True,
        editable=False,
    )
    inactive_reason = models.CharField(
        max_length=255,
        db_column='inactive_reason',
        editable=False,
    )
    created = models.DateTimeField(
        db_column='created_on',
        null=False,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='modified',
        null=True,
        editable=False,
    )
    deleted = models.DateTimeField(
        db_column='deleted',
        null=True,
        editable=False,
    )

    objects = JoinManager()

    # FKs
    subscription = models.ForeignKey(
        'Subscription',
        editable=False,
        related_name='joins',
        on_delete=models.CASCADE,
    )
    membership = models.ForeignKey(
        'Membership',
        editable=False,
        related_name='joins',
        on_delete=models.CASCADE,
    )

    structure = models.ForeignKey(
        'Structure',
        editable=False,
        related_name='joins',
        db_column='reference_structure_id',
        on_delete=models.CASCADE,
    )

    # Internals
    def clean(self):
        if all([
            not self.inactive_date,
            self.subscription.items_editable,
            self.subscription.status == 'expired',
        ]):
            raise ValidationError({
                'inactive_date': 'Inactive Date is missing on expired subscription.',
            })

    def __str__(self):
        return str(self.id)
        # return "{0} {1}".format(
        #     self.subscription,
        #     self.membership,
        # )

    class Meta:
        managed = False
        db_table = 'vwSubscriptions_Memberships'
        verbose_name = 'Join'
        verbose_name_plural = 'Joins'
