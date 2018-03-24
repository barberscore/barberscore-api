# Django
from django.db import models
from django.core.exceptions import ValidationError

from bhs.managers import StructureManager
from bhs.managers import SubscriptionManager
from bhs.managers import HumanManager
from bhs.managers import RoleManager
from bhs.managers import JoinManager
from django.utils.functional import cached_property


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
    email = models.CharField(
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
    sex = models.CharField(
        max_length=255,
        editable=False,
    )
    primary_voice_part = models.CharField(
        max_length=255,
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

    class Meta:
        managed=False
        db_table = 'vwMembers'


class Structure(models.Model):
    CHAPTER = 'chapter'
    DISTRICT = 'district'
    ORGANIZATION = 'organization'
    QUARTET = 'quartet'
    GROUP = 'group'

    KIND = [
        (ORGANIZATION, 'Organization'),
        (DISTRICT, 'District'),
        (GROUP, 'Group'),
        (CHAPTER, 'Chapter'),
        (QUARTET, 'Quartet'),
    ]

    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    kind = models.CharField(
        max_length=255,
        editable=False,
        choices=KIND,
        db_column='object_type',
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

    def clean(self):
        if not self.kind == 'quartet' or not self.status.name == 'active':
            return
        members = self.memberships.filter(
            joins__status=True,
        )
        count = members.count()
        if count != 4:
            raise ValidationError(
                {'status': 'Quartet member count is incorrect {0}'.format(count)}
            )

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

    objects = SubscriptionManager()

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
        managed=False
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
    vocal_part = models.CharField(
        max_length=255,
        editable=False,
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
    def __str__(self):
        return "{0} {1}".format(
            self.subscription,
            self.membership,
        )

    class Meta:
        managed=False
        db_table = 'vwSubscriptions_Memberships'
        verbose_name = 'Join'
        verbose_name_plural = 'Joins'
