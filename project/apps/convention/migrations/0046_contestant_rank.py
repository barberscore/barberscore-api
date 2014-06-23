# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0045_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='rank',
            field=models.IntegerField(help_text=b'\n            The incoming rank based on prelim score.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
