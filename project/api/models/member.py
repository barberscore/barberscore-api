
# Standard Library
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.apps import apps

# First-Party
from api.managers import MemberManager

log = logging.getLogger(__name__)


class Member(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        null=True,
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

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=False,
        db_index=True,
    )

    # Properties
    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='members',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='members',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='members',
    )

    # Internals
    objects = MemberManager()

    class Meta:
        unique_together = (
            ('group', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "member"

    def __str__(self):
        return str(self.id)

    def clean(self):
        return

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
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.group.officers.filter(
                    person__user=request.user,
                    status__gt=0,
                ),
                self.mc_pk == None,
            ]),
        ])

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Member."""
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Member."""
        return
