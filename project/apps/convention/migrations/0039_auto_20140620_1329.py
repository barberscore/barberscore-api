# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0038_performance_ordinal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.IntegerField(help_text=b'\n            The appearance order, within a given round.'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(help_text=b'\n            The approximate stagetime of the performance, in\n            the local time of the venue.  NOTE: for usage purposes,\n            the default is the current time.  However, this must\n            eventually be overwritten with the actual stagetime.', auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([(b'contest', b'contest_round', b'appearance')]),
        ),
    ]
