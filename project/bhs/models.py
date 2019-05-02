

# Third-Party
from model_utils import Choices

# Django
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models

# First-Party
from .managers import HumanManager
from .managers import JoinManager
from .managers import RoleManager
from .managers import StructureManager

from .fields import ValidatedPhoneField
from .fields import LowerEmailField
from .fields import ReasonableBirthDate
from .fields import VoicePartField
from .fields import NoPunctuationCharField

class Human(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    first_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
    )
    middle_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
        db_column='middle_initial',
    )
    last_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
    )
    nick_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
        db_column='preferred_name',
    )
    email = LowerEmailField(
        editable=False,
        null=True,
        db_column='username',
    )
    birth_date = ReasonableBirthDate(
        editable=False,
        null=True,
        db_column='birthday'
    )
    home_phone = ValidatedPhoneField(
        max_length=255,
        editable=False,
        db_column='phone'
    )
    cell_phone = ValidatedPhoneField(
        max_length=255,
        editable=False,
    )
    work_phone = ValidatedPhoneField(
        max_length=255,
        editable=False,
    )
    bhs_id = models.IntegerField(
        editable=False,
        unique=True,
        null=False,
        db_column='legacy_id',
    )
    GENDER = Choices(
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(
        max_length=255,
        editable=False,
        choices=GENDER,
        db_column='sex',
    )
    PART = Choices(
        ('tenor', 'Tenor'),
        ('lead', 'Lead'),
        ('baritone', 'Baritone'),
        ('bass', 'Bass'),
    )
    part = VoicePartField(
        max_length=255,
        editable=False,
        choices=PART,
        db_column='primary_voice_part',
    )
    mon = models.IntegerField(
        editable=False,
        db_column='trusted_mon',
    )
    is_deceased = models.BooleanField(
        editable=False,
    )
    is_honorary = models.BooleanField(
        editable=False,
        db_column='honorary_member',
    )
    is_suspended = models.BooleanField(
        editable=False,
    )
    is_expelled = models.BooleanField(
        editable=False,
    )
    merged_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='merged_into',
    )
    deleted_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='deleted_by_id',
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

    # Internals
    def __str__(self):
        if self.nick_name:
            first = self.nick_name
        else:
            first = self.first_name
        return " ".join([
            first,
            self.last_name,
        ])

    # Methods
    # def update_bs(self):
    #     Person = apps.get_model('api.person')
    #     Member = apps.get_model('api.member')
    #     Officer = apps.get_model('api.officer')
    #     Person.objects.update_or_create_from_human(self)
    #     joins = self.get_joins()
    #     for join in joins:
    #         Member.objects.update_or_create_from_join(join)
    #     roles = self.get_roles()
    #     for role in roles:
    #         Officer.objects.update_or_create_from_role(role)
    #     return

    # def get_joins(self):
    #     Join = apps.get_model('bhs.join')
    #     structures = self.subscriptions.prefetch_related(
    #         'joins__structure',
    #     ).values_list(
    #         'joins__structure',
    #         flat=True,
    #     ).distinct()
    #     joins = []
    #     for structure in structures:
    #         try:
    #             join = Join.objects.select_related(
    #                 'subscription__human',
    #                 'structure',
    #             ).filter(
    #                 paid=True,
    #                 deleted__isnull=True,
    #                 subscription__human=self,
    #                 structure__id=structure,
    #             ).latest(
    #                 'modified',
    #                 '-inactive_date',
    #             )
    #         except Join.DoesNotExist:
    #             continue
    #         joins.append(join)
    #     return joins

    # def get_roles(self):
    #     pairs = self.roles.select_related(
    #         'structure',
    #     ).values_list(
    #         'structure',
    #         'name',
    #     ).distinct()
    #     roles = []
    #     for structure, name in pairs:
    #         role = self.roles.select_related(
    #             'structure',
    #         ).filter(
    #             structure__id=structure,
    #             name=name,
    #         ).latest(
    #             'modified',
    #             '-end_date',
    #         )
    #         roles.append(role)
    #     return roles

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
    DIVISION = Choices(
        ('EVG', [
            'EVG Division I',
            'EVG Division II',
            'EVG Division III',
            'EVG Division IV',
            'EVG Division V',
        ]),
        ('FWD', [
            'FWD Arizona',
            'FWD Northeast',
            'FWD Northwest',
            'FWD Southeast',
            'FWD Southwest',
        ]),
        ('LOL', [
            'LOL 10000 Lakes',
            'LOL Division One',
            'LOL Northern Plains',
            'LOL Packerland',
            'LOL Southwest',
        ]),
        ('MAD', [
            # (160, 'madatl', 'MAD Atlantic'),
            'MAD Central',
            'MAD Northern',
            'MAD Southern',
            # (200, 'madwst', 'MAD Western'),
        ]),
        ('NED', [
            'NED Granite and Pine',
            'NED Mountain',
            'NED Patriot',
            'NED Sunrise',
            'NED Yankee',
        ]),
        ('SWD', [
            'SWD Northeast',
            'SWD Northwest',
            'SWD Southeast',
            'SWD Southwest',
        ]),
    )
    division = models.CharField(
        max_length=255,
        editable=False,
        null=True,
        db_column='division',
        choices=DIVISION,
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
    website = models.CharField(
        max_length=255,
        editable=False,
    )
    email = models.CharField(
        max_length=255,
        editable=False,
    )
    chorus_name = models.CharField(
        max_length=255,
        editable=False,
    )
    phone = models.CharField(
        max_length=255,
        editable=False,
    )
    fax = models.CharField(
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
    youtube = models.CharField(
        max_length=255,
        editable=False,
    )
    pinterest = models.CharField(
        max_length=255,
        editable=False,
    )
    flickr = models.CharField(
        max_length=255,
        editable=False,
    )
    instagram = models.CharField(
        max_length=255,
        editable=False,
    )
    soundcloud = models.CharField(
        max_length=255,
        editable=False,
    )
    tin = models.CharField(
        max_length=18,
        editable=False,
    )
    preferred_name = models.CharField(
        max_length=255,
        editable=False,
    )
    first_alternate_name = models.CharField(
        max_length=255,
        editable=False,
    )
    second_alternate_name = models.CharField(
        max_length=255,
        editable=False,
    )
    visitor_information = models.TextField(
        editable=False,
    )
    established_date = models.DateField(
        editable=False,
    )
    chartered_date = models.DateField(
        editable=False,
    )
    licenced_date = models.DateField(
        editable=False,
    )
    deleted_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='deleted_by_id',
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
        # editable=False,
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


    # def update_bs(self):
    #     if self.kind not in [self.KIND.chorus, self.KIND.quartet,]:
    #         raise ValueError("Only choruses and quartets may be updated")
    #     Group = apps.get_model('api.group')
    #     Member = apps.get_model('api.member')
    #     Officer = apps.get_model('api.officer')
    #     Group.objects.update_or_create_from_structure(self)
    #     joins = self.get_joins()
    #     for join in joins:
    #         Member.objects.update_or_create_from_join(join)
    #     roles = self.get_roles()
    #     for role in roles:
    #         Officer.objects.update_or_create_from_role(role)
    #     return


    # def get_joins(self):
    #     humans = self.joins.select_related(
    #         'subscription__human',
    #     ).values_list(
    #         'subscription__human',
    #         flat=True,
    #     ).distinct()
    #     joins = []
    #     for human in humans:
    #         try:
    #             join = self.joins.select_related(
    #                 'subscription',
    #                 'subscription__human',
    #             ).filter(
    #                 paid=True,
    #                 deleted__isnull=True,
    #                 subscription__human__id=human,
    #             ).latest(
    #                 'modified',
    #                 '-inactive_date',
    #             )
    #         except self.joins.model.DoesNotExist:
    #             continue
    #         joins.append(join)
    #     return joins

    # def get_roles(self):
    #     pairs = self.roles.select_related(
    #         'human',
    #     ).values_list(
    #         'human',
    #         'name',
    #     ).distinct()
    #     roles = []
    #     for human, name in pairs:
    #         role = self.roles.select_related(
    #             'human',
    #         ).filter(
    #             human__id=human,
    #             name=name,
    #         ).latest(
    #             'modified',
    #             '-end_date',
    #         )
    #         roles.append(role)
    #     return roles

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
    deleted_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='deleted_by_id',
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
    deleted = models.DateTimeField(
        null=False,
        editable=False,
        db_column='deleted',
    )
    created = models.DateTimeField(
        null=False,
        editable=False,
        db_column='created',
    )
    modified = models.DateTimeField(
        null=True,
        editable=False,
        db_column='updated',
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
    part = VoicePartField(
        max_length=255,
        editable=False,
        choices=PART,
        db_column='vocal_part',
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
    deleted = models.DateTimeField(
        null=False,
        editable=False,
        db_column='deleted',
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
