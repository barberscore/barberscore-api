import uuid
from django_pg import models
from django.core.urlresolvers import reverse

from django.core.validators import (
    RegexValidator,
)

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName


class Singer(models.Model):
    """An individual singer."""
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    full_name = models.CharField(
        verbose_name="Full Name",
        help_text="""
            The Full Name of the Singer.""",
        blank=True,
        null=True,
        max_length=100,
    )

    mobile = PhoneNumberField(
        verbose_name='mobile number',
        help_text="""
            The Full Name of the Singer.""",
        unique=True,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name="Email Address",
        help_text="""
            The Email Address of the User.""",
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    timezone = TimeZoneField(
        default='US/Pacific',
    )

    @property
    def first_name(self):
        if self.full_name:
            name = HumanName(self.full_name)
            return name.first
        else:
            return None

    @property
    def last_name(self):
        if self.full_name:
            name = HumanName(self.full_name)
            return name.last
        else:
            return None

    def __unicode__(self):
        if self.full_name:
            return "{0}".format(self.full_name)
        else:
            return self.id


class Chorus(models.Model):
    """An individual singer."""
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the chorus.""",
        max_length=200,
    )

    slug = models.SlugField(
        help_text="""
            The slug, generated in a signal from the name field.""",
        max_length=200,
        unique=True,
        blank=True,
        null=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the contestant.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the contestant.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the contestant.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the contestant.""",
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
            The contact email of the contestant.""",
        blank=True,
    )

    mobile = PhoneNumberField(
        verbose_name='mobile number',
        help_text="""
            The Full Name of the Singer.""",
        unique=True,
        blank=True,
        null=True,
    )

    director = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    district = models.IntegerField(
        help_text="""
            The district the
            contestant is representing.""",
        blank=True,
        null=True,
        # default=UNK,
        # choices=DISTRICT_CHOICES,
    )

    # prelim = models.FloatField(
    #     help_text="""
    #         The prelim score of the contestant.""",
    #     null=True,
    #     blank=True,
    # )

    # rank = models.IntegerField(
    #     help_text="""
    #         The incoming rank based on prelim score.""",
    #     null=True,
    #     blank=True,
    # )

    picture = models.ImageField(
        help_text="""
            The 'official' picture of the contestant.""",
        blank=True,
        null=True,
    )

    blurb = models.TextField(
        help_text="""
            A blurb describing the contestant.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chorus', args=[str(self.slug)])

    class Meta:
        ordering = ['name']
