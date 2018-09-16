
# Standard Library
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.db import models
from django.utils.functional import cached_property

log = logging.getLogger(__name__)


class Office(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
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
        ('Group', [
            (32, 'chapter', "Chapter"),
            (41, 'quartet', "Quartet"),
        ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of office.""",
        choices=KIND,
        null=True,
        blank=True,
    )

    CODE = Choices(
        ('International', [
            (100, 'scjc_chair', "SCJC Chair"),
            (110, 'scjc_past', "SCJC Chair Past"),
            (120, 'scjc_ca', "SCJC CA"),
            (130, 'scjc_mus', "SCJC MUS"),
            (140, 'scjc_per', "SCJC PER"),
            (150, 'scjc_sng', "SCJC SNG"),
            (160, 'scjc_chart', "SCJC Chart"),
            (170, 'scjc_admin', "SCJC Admin"),
        ]),
        ('District', [
            (210, 'drcj', "DRCJ"),
            (220, 'drcj_asst', "DRCJ Assistant"),
            (230, 'judge_ca', "JUDGE CA"),
            (240, 'judge_mus', "JUDGE MUS"),
            (250, 'judge_per', "JUDGE PER"),
            (260, 'judge_sng', "JUDGE SNG"),
            (270, 'candidate_ca', "CANDIDATE CA"),
            (280, 'candidate_mus', "CANDIDATE MUS"),
            (290, 'candidate_per', "CANDIDATE PER"),
            (295, 'candidate_sng', "CANDIDATE SNG"),
        ]),
        ('Group', [
            (310, 'chap_pres', "CPRES"),
            (320, 'chap_sec', "CSEC"),
            (320, 'chap_dir', "CDIR"),
            (340, 'chap_asst', "CASS"),
            (350, 'chap_man', "CMAN"),
            (410, 'quartet_admin', "QADM"),
        ]),
    )

    code = models.IntegerField(
        help_text="""
            The short-form office code.""",
        choices=CODE,
        null=True,
        blank=True,
    )

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=True,
        db_index=True,
    )

    # Office Permissions
    is_convention_manager = models.BooleanField(
        default=False,
    )

    is_session_manager = models.BooleanField(
        default=False,
    )

    is_round_manager = models.BooleanField(
        default=False,
    )

    is_scoring_manager = models.BooleanField(
        default=False,
    )

    is_group_manager = models.BooleanField(
        default=False,
    )

    is_person_manager = models.BooleanField(
        default=False,
    )

    is_award_manager = models.BooleanField(
        default=False,
    )

    is_officer_manager = models.BooleanField(
        default=False,
    )

    is_chart_manager = models.BooleanField(
        default=False,
    )

    is_assignment_manager = models.BooleanField(
        default=False,
    )

    # Properties
    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

    # Internals
    class Meta:
        ordering = ['code']

    class JSONAPIMeta:
        resource_name = "office"

    def __str__(self):
        return self.name

    # Office Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False
