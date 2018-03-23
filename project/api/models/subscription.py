# Standard Libary
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


log = logging.getLogger(__name__)


class Subscription(TimeStampedModel):
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
        (10, 'RG', 'RG Regular'),
        (20, 'R5', 'R5 Regular 50 Year'),
        (30, 'SN', 'SN Senior'),
        (40, 'S5', 'S5 Senior 50 Year'),
        (50, 'SL', 'SL Senior Legacy'),
        (60, 'Y1', 'Y1 Youth Initial'),
        (70, 'Y2', 'Y2 Youth Subsequent'),
        (80, 'LF', 'LF Lifetime Regular'),
        (90, 'L5', 'L5 Lifetime 50 Year'),
        (100, 'LY', 'LY Lifetime Youth'),
        (110, 'LS', 'LS Lifetime Senior'),
        (120, 'AS', 'AS Associate'),
    )

    code = models.IntegerField(
        help_text="""
            The subscription code.""",
        choices=CODE,
        null=True,
        blank=True,
    )

    mc_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    # Properties
    # Internals

    class Meta:
        ordering = ['code']

    class JSONAPIMeta:
        resource_name = "subscription"

    def __str__(self):
        return self.name

    # Office Permissions
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
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return True
