import uuid
import datetime
import operator
from io import BytesIO

# Third-Party
from model_utils import Choices
from django_fsm import FSMIntegerField
from model_utils.models import TimeStampedModel
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from phonenumber_field.modelfields import PhoneNumberField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from timezone_field import TimeZoneField
from docx import Document

# Django
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property
from django.conf import settings
from django.contrib.postgres.fields import DecimalRangeField
from django.contrib.postgres.fields import IntegerRangeField
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models import Case, When, Q, Count
from django.template.defaultfilters import pluralize

from .fields import ImageUploadPath
from .fields import UploadPath


class Organization(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            e.g. Barbershop Harmony Society""",
        max_length=255,
        default='',
    )

    abbreviation = models.CharField(
        help_text="""
            e.g. BHS""",
        max_length=255,
    )

    logo = models.FileField(
        upload_to=UploadPath('organization_logos'),
        help_text="""Logo should be 108px x 108px in JPG format.""",
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
    )

    district_nomen = models.CharField(
        help_text="""String that should be used to replace "District" references on reports.""",
        max_length=255,
        default='District',
    )

    division_nomen = models.CharField(
        help_text="""String that should be used to replace "Division" references on reports.""",
        max_length=255,
        default='Division',
    )

    drcj_nomen = models.CharField(
        help_text="""String that should be used to replace "DRCJ" references on reports.""",
        max_length=255,
        default='DRCJ',
        verbose_name="DRCJ nomen",
    )

    default_owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='organizations',
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='divisions',
    )

    # Properties
    @cached_property
    def nomen(self):
        return self.name

    def __str__(self):
        return self.nomen


class District(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='organization',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        help_text="""
            e.g. Far Western District""",
        max_length=255,
        default='',
        verbose_name="District Name",
    )

    abbreviation = models.CharField(
        help_text="""
            e.g. FWD""",
        max_length=255,
    )

    logo = models.FileField(
        upload_to=UploadPath('district_logos'),
        help_text="""Logo should be xx x xx in JPG format.""",
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='divisions',
    )

    # Properties
    @cached_property
    def nomen(self):
        return self.name

    def __str__(self):
        return self.nomen


class Division(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    district = models.ForeignKey(
        'District',
        related_name='district',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        help_text="""
            e.g. FWD Northwest""",
        max_length=255,
        default='',
        verbose_name="Division Name",
    )

    abbreviation = models.CharField(
        help_text="""
            e.g. fwdnw""",
        max_length=255,
    )

    logo = models.FileField(
        upload_to=UploadPath('division_logos'),
        help_text="""Logo should be xx x xx in JPG format.""",
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='divisions',
    )

    # Properties
    @cached_property
    def nomen(self):
        return self.name

    def __str__(self):
        return self.nomen
