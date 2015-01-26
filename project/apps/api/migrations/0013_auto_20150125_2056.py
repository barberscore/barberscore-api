# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_quartet_old_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegiate',
            name='district',
        ),
        migrations.RemoveField(
            model_name='collegiate',
            name='members',
        ),
        migrations.RemoveField(
            model_name='collegiatemembership',
            name='collegiate',
        ),
        migrations.RemoveField(
            model_name='collegiatemembership',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='collegiatemembership',
            name='singer',
        ),
        migrations.DeleteModel(
            name='CollegiateMembership',
        ),
        migrations.RemoveField(
            model_name='collegiateperformance',
            name='collegiate',
        ),
        migrations.DeleteModel(
            name='Collegiate',
        ),
        migrations.RemoveField(
            model_name='collegiateperformance',
            name='contest',
        ),
        migrations.DeleteModel(
            name='CollegiatePerformance',
        ),
    ]
