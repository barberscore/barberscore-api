# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0026_remove_performance_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='twitter',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
