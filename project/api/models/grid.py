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
from django.apps import apps as api_apps
from django.contrib.postgres.fields import ArrayField
from django.db import models

config = api_apps.get_app_config('api')

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
        'Round',
        related_name='grids',
        on_delete=models.CASCADE,
    )

    competitor = models.ForeignKey(
        'Competitor',
        related_name='grids',
        on_delete=models.CASCADE,
    )

    appearance = models.OneToOneField(
        'Appearance',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        unique_together = (
            ('round', 'competitor',),
        )

    class JSONAPIMeta:
        resource_name = "grid"

    def __str__(self):
        return "{0} {1}".format(
            self.round,
            self.competitor,
        )

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return True
        # return any([
        #     request.user.is_convention_manager,
        # ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return True
        # return any([
        #     self.round.session.convention.assignments.filter(
        #         person__user=request.user,
        #         category__lt=30,
        #         kind=10,
        #     ),
        # ])
