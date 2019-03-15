import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices
from django_fsm import FSMIntegerField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from .validators import validate_bhs_id
from .validators import validate_birth_date
from .managers import PersonManager

class Person(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    STATUS = Choices(
        (-20, 'new', 'Expelled'),
        (-10, 'suspended', 'Suspended'),
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
    )
    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )
    prefix = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
    )
    middle_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
    )
    suffix = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    nick_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        validators=[
            validate_birth_date,
        ],
    )
    is_deceased = models.BooleanField(
        default=False,
    )
    home_phone = PhoneNumberField(
        default='',
        blank=True,
    )
    cell_phone = PhoneNumberField(
        default='',
        blank=True,
    )
    work_phone = PhoneNumberField(
        default='',
        blank=True,
    )
    bhs_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        validators=[
            validate_bhs_id,
        ],
    )
    GENDER = Choices(
        (10, 'male', 'Male'),
        (20, 'female', 'Female'),
    )
    gender = FSMIntegerField(
        null=True,
        blank=True,
        choices=GENDER,
    )
    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )
    part = FSMIntegerField(
        null=True,
        blank=True,
        choices=PART,
    )
    mon = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(999),
        ],
    )

    objects = PersonManager()

    # Internals
    def __str__(self):
        return "{0}".format(
            self.id,
        )

    class Meta:
        pass
