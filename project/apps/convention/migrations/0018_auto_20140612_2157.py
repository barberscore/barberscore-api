# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0017_auto_20140612_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contestant',
            name='blurb',
            field=models.TextField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
