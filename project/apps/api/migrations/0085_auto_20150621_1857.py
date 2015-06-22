# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_remove_song_arrangement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='singer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, blank=True),
        ),
    ]
