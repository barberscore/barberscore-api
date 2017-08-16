from django.db import models
import uuid

class Membership(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
    )

    first_name = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        max_length=255,
        editable=False,
    )
    last_name = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        max_length=255,
    )
    # Internals
    class Meta:
        db_table = 'vwMembers'
