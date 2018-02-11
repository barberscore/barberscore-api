# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps as api_apps
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
# First-Party
from api.fields import CloudinaryRenameField
from api.managers import GroupManager

api = api_apps.get_app_config('api')
bhs = api_apps.get_app_config('bhs')

log = logging.getLogger(__name__)


class Group(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.
        """,
        max_length=255,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (-5, 'aic', 'AIC',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        ('International', [
            (1, 'international', "International"),
        ]),
        ('District', [
            (11, 'district', "District"),
            (12, 'noncomp', "Noncompetitive"),
            (13, 'affiliate', "Affiliate"),
        ]),
        ('Division', [
            (21, 'division', "Division"),
        ]),
        ('Chapter', [
            (30, 'chapter', "Chapter"),
        ]),
        ('Group', [
            (32, 'chorus', "Chorus"),
            (41, 'quartet', "Quartet"),
        ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group.
        """,
        choices=KIND,
    )

    GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    gender = models.IntegerField(
        help_text="""
            The gender of group.
        """,
        choices=GENDER,
        default=GENDER.male,
    )

    short_name = models.CharField(
        help_text="""
            A short-form name for the resource.""",
        blank=True,
        max_length=255,
    )

    code = models.CharField(
        help_text="""
            The chapter code.""",
        max_length=255,
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the resource.""",
        blank=True,
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'@([A-Za-z0-9_]+)',
                message="""
                    Must be a single Twitter handle
                    in the form `@twitter_handle`.
                """,
            ),
        ],
    )

    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
    )

    phone = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A description of the group.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    MEM_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'active_internal', 'Active Internal',),
        (30, 'active_licensed', 'Active Licensed',),
        (40, 'cancelled', 'Cancelled',),
        (50, 'closed', 'Closed',),
        (60, 'closed_merged', 'Closed Merged',),
        (70, 'closed_revoked', 'Closed Revoked',),
        (80, 'closed_voluntary', 'Closed Voluntary',),
        (90, 'expelled', 'Expelled',),
        (100, 'expired', 'Expired',),
        (105, 'expired_licensed', 'Expired Licensed',),
        (110, 'lapsed', 'Lapsed',),
        (120, 'not_approved', 'Not Approved',),
        (130, 'pending', 'Pending',),
        (140, 'pending_voluntary', 'Pending Voluntary',),
        (150, 'suspended', 'Suspended',),
        (160, 'suspended_membership', 'Suspended Membership',),
    )

    mem_status = models.IntegerField(
        choices=MEM_STATUS,
        null=True,
        blank=True,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    # FKs
    parent = models.ForeignKey(
        'Group',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_index=True,
    )

    # Denormalizations
    tree_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    international = models.TextField(
        help_text="""
            The denormalized international organization.""",
        blank=True,
        max_length=255,
    )

    district = models.TextField(
        help_text="""
            The denormalized district organization.""",
        blank=True,
        max_length=255,
    )

    division = models.TextField(
        help_text="""
            The denormalized division organization.""",
        blank=True,
        max_length=255,
    )

    chapter = models.TextField(
        help_text="""
            The denormalized chapter organization.""",
        blank=True,
        max_length=255,
    )

    is_senior = models.BooleanField(
        help_text="""Qualifies as a Senior Group.  This is set once, at creation.  If the group 'ages' into Senior status that needs to be edited manually here.""",
        default=False,
    )

    # Internals
    objects = GroupManager()

    class Meta:
        verbose_name_plural = 'groups'

    class JSONAPIMeta:
        resource_name = "group"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        pass
        # if self.kind == self.KIND.quartet:
        #     if self.organization.kind != self.organization.KIND.quartet:
        #         raise ValidationError(
        #             {'kind': 'Quartets kind must match organization kind.'}
        #         )
        # else:
        #     if self.organization.kind != self.organization.KIND.chapter:
        #         raise ValidationError(
        #             {'kind': 'Choruses kind must match organization kind.'}
        #         )

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super().save(*args, **kwargs)

    # Methods
    def update_from_chapter(self):
        if self.kind != self.KIND.chorus:
            raise ValueError("Can only update choruses")
        if self.status != self.STATUS.active:
            raise ValueError("Can only update active choruses")
        # Copy from chapter.
        chapter = self.organization
        if chapter.kind != chapter.KIND.chapter:
            raise ValueError("Must have chapter as parent")
        self.email = chapter.email
        self.phone = chapter.phone
        self.website = chapter.website
        self.facebook = chapter.facebook
        self.twitter = chapter.twitter
        self.bhs_id = chapter.bhs_id
        self.bhs_pk = chapter.bhs_pk
        if chapter.status < 0:
            self.status = self.STATUS.inactive
        self.save()
        return

    def update_memberships(self):
        if self.kind != self.KIND.quartet:
            raise RuntimeError("Can only update quartets")
        if not self.bhs_pk:
            raise RuntimeError("No BHS Link.")
        Member = api.get_model('Member')
        Structure = bhs.get_model('Structure')
        structure = Structure.objects.get(id=self.bhs_pk)
        js = structure.smjoins.values(
            'subscription__human',
            'structure',
        ).distinct()

        for j in js:
            m = structure.smjoins.filter(
                subscription__human__id=j['subscription__human'],
                structure__id=j['structure'],
            ).latest('established_date', 'updated_ts')
            Member.objects.update_or_create_from_join(m)
        return

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.organization.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Group."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Group."""
        return
