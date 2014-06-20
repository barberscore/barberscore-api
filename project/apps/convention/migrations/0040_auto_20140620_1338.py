# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0039_auto_20140620_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text=b'\n            The approximate stagetime of the performance, in\n            the local time of the venue.  NOTE: for usage purposes,\n            the default is the current time.  However, this must\n            eventually be overwritten with the actual stagetime.'),
        ),
    ]
