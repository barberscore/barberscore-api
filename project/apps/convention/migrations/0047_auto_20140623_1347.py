# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0046_contestant_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text=b'\n            The approximate stagetime of the performance, in\n            the local time of the venue. '),
        ),
    ]
