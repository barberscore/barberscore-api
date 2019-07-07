import logging
import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_fsm import FSMIntegerField
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from timezone_field import TimeZoneField

log = logging.getLogger(__name__)


class Grid(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    PERIOD = Choices(
        (1, 'one', 'One',),
        (2, 'two', 'Two',),
        (3, 'three', 'Three',),
    )

    period = models.IntegerField(
        null=True,
        blank=True,
        choices=PERIOD,
    )

    num = models.IntegerField(
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    photo = models.DateTimeField(
        null=True,
        blank=True,
    )

    arrive = models.DateTimeField(
        null=True,
        blank=True,
    )

    depart = models.DateTimeField(
        null=True,
        blank=True,
    )

    backstage = models.DateTimeField(
        null=True,
        blank=True,
    )

    onstage = models.DateTimeField(
        help_text="""
            The scheduled stage time in the Local time of the Venue.""",
        null=True,
        blank=True,
    )

    start = models.DateTimeField(
        help_text="""
            The actual start time.""",
        null=True,
        blank=True,
    )

    renditions = ArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=100,
        ),
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'rmanager.round',
        related_name='grids',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    venue = models.ForeignKey(
        'Venue',
        related_name='grids',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # appearance = models.OneToOneField(
    #     'Appearance',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    # )

    # Internals
    class JSONAPIMeta:
        resource_name = "grid"

    def __str__(self):
        return str(self.id)

    # Permissions
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
        return any([
            request.user.person.officers.filter(
                office__lt=200,
                status__gt=0,
            ),
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.person.officers.filter(
                office__lt=200,
                status__gt=0,
            ),
        ])


class Venue(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=255,
        default='(TBD)',
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

    city = models.CharField(
        max_length=255,
        blank=True,
    )

    state = models.CharField(
        max_length=255,
        blank=True,
    )

    airport = models.CharField(
        max_length=30,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the venue.""",
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='venues',
    )

    # Methods
    def __str__(self):
        return "{0} {1}, {2}".format(
            self.name,
            self.city,
            self.state,
        )

    # Internals
    class JSONAPIMeta:
        resource_name = "venue"

    # Permissions
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
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.person.officers.filter(
                office__lt=200,
                status__gt=0,
            ),
        ])

