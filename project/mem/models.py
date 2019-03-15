import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices
from django_fsm import FSMIntegerField
from phonenumber_field.modelfields import PhoneNumberField

class Person(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    STATUS = Choices(
        (0, 'new', 'New',),
    )
    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )
    prefix = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    middle_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    suffix = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    nick_name = models.CharField(
        max_length=255,
        null=True,
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
    )
    is_deceased = models.BooleanField(
        default=False,
    )
    home_phone = PhoneNumberField(
        null=True,
        blank=True,
    )
    cell_phone = PhoneNumberField(
        null=True,
        blank=True,
    )
    work_phone = PhoneNumberField(
        null=True,
        blank=True,
    )
    bhs_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
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
        null=False,
        blank=True,
    )

    # Internals
    def __str__(self):
        return "{0}".format(
            self.id,
        )

    class Meta:
        pass
